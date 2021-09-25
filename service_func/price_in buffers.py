import itertools

import pyproj
import pandas as pd
import geopandas as gpd
import numpy as np

from tqdm.auto import tqdm
from joblib import Parallel, delayed
from functools import partial
from shapely.geometry import Point
from shapely.ops import transform

TRAIN_PATH = 'data/train.csv'
TEST_PATH = 'data/test.csv'
OUT_PATH = 'prices.csv'


def spatial_points(df, lat, lon):
    """Confert PandasDataFrame to GeoDataFrame."""
    geometry = [Point(xy) for xy in zip(df[lon], df[lat])]
    gdf = gpd.GeoDataFrame(df, crs={'init': 'epsg:4326'}, geometry=geometry)
    return gdf


def geodesic_point_buffer(lon, lat, km):
    """Create geodesic buffer around a given point (lat, lon)."""
    # Azimuthal equidistant projection
    proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')
    aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
    project = partial(
        pyproj.transform,
        pyproj.Proj(aeqd_proj.format(lon=lon, lat=lat)),
        proj_wgs84)
    buf = Point(0, 0).buffer(km * 1000)  # distance in metres
    return transform(project, buf)


def geodesic_buffer(df, radius):
    """Apply geodesic_point_buffer to PandasDataFrame  and convert to GeoDataFrame."""
    geom = df.apply(lambda row: geodesic_point_buffer(row['lng'], row['lat'], radius / 1000), axis=1)
    buffers = df.copy()
    buffers = gpd.GeoDataFrame(buffers, geometry=geom, crs={'init': 'epsg:4326'})
    buffers = buffers[['id', 'geometry']]
    return buffers


def get_batches(df, batch_size=1000):
    """Get list of batches for input PandasDataFrame"""
    batch_nums = int(np.ceil(df.shape[0] / batch_size))
    batches = [df[batch_size * i:batch_size * i + batch_size] for i in range(batch_nums)]
    return batches


def spatial_join(data):
    """Spatial joi function for Parallel processing"""
    df_a = data[0]
    df_b = data[1]
    return gpd.sjoin(df_a, df_b)


def price_stat_in_buffers(df, buffer_radius=[100, 250, 500, 1000, 5000]):
    out = df[['id']]
    for radius in tqdm(buffer_radius):
        all_types = []
        for realty_type in df['realty_type'].unique():
            df_realty_type = df[df['realty_type'] == realty_type]

            buffers = Parallel(n_jobs=-1)(delayed(geodesic_buffer)(i, radius) for i in get_batches(df_realty_type))
            buffers = pd.concat(buffers)
            points = df_realty_type.copy()
            points = points[points['price_type'] == 0]
            points = spatial_points(points, lat='lat', lon='lng')
            points = points.drop(['price_type', 'realty_type', 'lat', 'lng'], axis=1)

            stat = Parallel(n_jobs=-1)(delayed(spatial_join)(i)
                                       for i in itertools.product(get_batches(points, batch_size=30000),
                                                                  get_batches(buffers, batch_size=30000)
                                                                  )
                                       )
            stat = pd.concat(stat)
            stat = stat[stat['id_left'] != stat['id_right']]
            stat = stat[['id_right', 'per_square_meter_price']]
            stat.columns = ['id', 'price']
            stat = stat.groupby('id').agg([np.mean, np.std, np.median, np.min, np.max])
            stat = stat.reset_index()
            stat.columns = ['_'.join(i) + '_r_{}'.format(radius) if 'id' not in i else 'id' for i in stat.columns]

            all_types.append(stat)
        all_types = pd.concat(all_types)
        out = out.merge(all_types, on='id', how='left')
        # out.to_csv(OUT_PATH, index=False)
    return out


def main():
    train = pd.read_csv(TRAIN_PATH)
    test = pd.read_csv(TEST_PATH)
    df = pd.concat([train, test])
    df = df[['id', 'lat', 'lng', 'price_type', 'realty_type', 'per_square_meter_price']]
    price_stat_in_buffers(df).to_csv(OUT_PATH, index=False)


if __name__ == "__main__":
    main()
