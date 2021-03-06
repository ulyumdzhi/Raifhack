FEDERAL_DISTRICT = {
    # ЦЕНТРАЛЬНЫЙ ФО
    1: ["Москва",
          "Московская область",
          "Тверская область",
          "Смоленская область",
          "Калужская область",
          "Брянская область",
          "Тульская область",
          "Орловская область",
          "Рязанская область",
          "Владимирская область",
          "Ивановская область",
          "Костромская область",
          "Ярославская область",
          "Курская область",
          "Белгородская область",
          "Липецкая область",
          "Воронежская область",
          "Тамбовская область"],
    # СЕВЕРО-ЗАПАДНЫЙ ФО
    2: ["Санкт-Петербург",
          "Ленинградская область",
          "Новгородская область",
          "Псковская область",
          "Вологодская область",
          "Карелия",
          "Мурманская область",
          "Архангельская область",
          "Ненецкий АО",
          "Коми",
          "Калининградская область"],
    # ПРИВОЛЖСКИЙ ФО
    3: ["Нижегородская область",
          "Кировская область",
          "Республика Марий Эл",
          "Чувашская Республика",
          "Мордовия",
          "Татарстан",
          "Ульяновская область",
          "Пензенская область",
          "Саратовская область",
          "Самарская область",
          "Пермский край",
          "Удмуртия",
          "Татарстан",
          "Башкортостан",
          "Оренбургская область"],
    # ЮЖНЫЙ ФО
    4: ["Волгоградская область",
          "Астраханская область ",
          "Калмыкия",
          "Ростовская область",
          "Краснодарский край",
          "Адыгея",
          "Крым",
          "Севастополь "],
    # СЕВЕРО-КАВКАЗСКИЙ ФО
    5: ["Ставропольский край",
          "Карачаево-Черкесская Республика",
          "Кабардино-Балкарская Республика",
          "Республика Северная Осетия - Алания ",
          "Республика Ингушетия",
          "Республика Чечня",
          "Республика Дагестан"],
    # УРАЛЬСКИЙ ФО
    6: ["Свердловская область",
          "Челябинская область",
          "Курганская область",
          "Тюменская область",
          "Ханты-Мансийский АО",
          "Ямало-Ненецкий АО"],
    # СИБИРСКИЙ ФО
    7: ["Омская область",
          "Томская область",
          "Новосибирская область",
          "Кемеровская область",
          "Алтайский край",
          "Алтай",
          "Красноярский край",
          "Хакасия",
          "Тыва",
          "Иркутская область"],
    # ДАЛЬНЕВОСТОЧНЫЙ ФО
    8: ["Республика Бурятия",
          "Забайкальский край",
          "Саха",
          "Магаданская область",
          "Чукотский автономный округ",
          "Камчатский край",
          "Амурская область",
          "Еврейская автономная область",
          "Хабаровский край",
          "Приморский край",
          "Сахалинская область"]}

# def get_federal_district(df: pd.DataFrame) -> pd.DataFrame:
#     df['federal_district'] = [str([key for key, val in federal_district.items() if row in val]) if row == row else None for row in df['region']]
#     df['federal_district'] = [i[1] for i in df['federal_district']]
#     df['federal_district'] = df['federal_district'].astype(int)
#     return df
      





