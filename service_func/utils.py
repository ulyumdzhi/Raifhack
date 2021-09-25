import pandas as pd

curs = [
        'USD', # доллар США
        'EUR', # Евро
        'UAH' # Украинская гривна
       ]

CBR_CUR_URL = 'https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To={}'

def get_exchange_rate(df: pd.DataFrame, currency: list, url: str = CBR_CUR_URL) -> pd.DataFrame:
    """
    Получает курсы валют с сайта ЦБР по тем датам, которые есть в датафрейме
    
    :param df: dataframe, выборка
    :param currency: list, список буквенных кодов валют
    :param url: str, url запроса на сайте ЦБ
    :return: dataframe
    """  
    res = pd.DataFrame(df.date.unique(), columns=['date'])
    
    for c in currency:
        c_df = []
        for date in res.values:
            tmp = pd.read_html(url.format(pd.to_datetime(date[0]).strftime('%d.%m.%Y')))[0]
            cur = tmp[tmp['Букв. код']==c]['Курс'].values[0]
            c_df.append(cur)
        res[c] = [i/10000 for i in c_df]
    
    return res

# get_exchange_rate(df, curs)

def get_investments_data_for_region(df: pd.DataFrame) -> pd.DataFrame:
    
    """
    Формируем таблицу по инвестиционной привлекательности регионов
    
    :param: df: dataframe, выборка
    :retern: dataframe
    
    Ранг риска, 2019
    Доля в общероссийском потенциале, 2019 год (%)
    Ранг, потенциала 2019',
    Среднезавшенный индекс риска, 2019 год

    источник*: https://raex-a.ru/files/REG_2019_Analytica_Block_Web.pdf
    
    *но более простой вариант получить таблицу с сайта kommersant.ru
    """
    
    def region_replacer(region: str) -> str:
        """
        Приводим названия регионов к общему виду
        """
        region = region.replace('Г. ', '').replace('Республика ', '')
        rep = {'Удмуртская Республика': 'Удмуртия', 'Ханты-Мансийский автономный округ — Югра':'Ханты-Мансийский АО'}
        if region in rep:
            region = rep[region]
        
        return region

    url = 'https://www.kommersant.ru/doc/4196717'

    tmp = pd.read_html(url, encoding='utf-8')[4]
    tmp = tmp[['Регион (субъект федерации)', 
               'Ранг риска, 2019', 
               'Доля в общероссийском потенциале, 2019 год (%)']].dropna()
    tmp = pd.DataFrame({'region':  [region_replacer(i) for i in tmp.iloc[:, 0]], 
                        'risk_rank_2019': tmp.iloc[:, 1].astype('Int64'), 
                        'potential_percent_2019': tmp.iloc[:, 2]/10})
    
    tmp2 = pd.read_html(url, encoding='utf-8')[2][['Регион (субъект федерации)', 
                                                   'Ранг, потенциала 2019',
                                                   'Среднезавшенный индекс риска, 2019 год']].dropna()
    tmp2 = pd.DataFrame({'region': [region_replacer(i) for i in tmp2.iloc[:, 0]], 
                         'potential_rank_2019': tmp2.iloc[:, 1].astype('Int64'), 
                         'weighted_risk_2019': tmp2.iloc[:, 2]/1000})
    
    res = tmp.merge(tmp2, on='region', how='left')
    
    return res 








