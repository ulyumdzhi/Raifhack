def city_class(city):

    capitals = ['Москва','Санкт-Петербург']
    millioneers = ['Новосибирск','Екатеринбург','Казань','Нижний Новгород','Челябинск','Самара','Омск','Ростов-на-Дону','Уфа','Красноярск','Воронеж','Пермь','Волгоград']
    biggest_cities = ['Астрахань','Балашиха','Барнаул','Владивосток','Ижевск','Иркутск','Кемерово','Киров','Краснодар','Липецк','Махачкала','Набережные Челны','Новокузнецк','Оренбург','Пенза','Рязань','Саратов','Севастополь','Тольятти','Томск','Тюмень','Ульяновск','Хабаровск','Ярославль']
    if any(city in s for s in capitals):
        return 'capitals'
    if any(city in s for s in millioneers):
        return 'millioneers'
    if any(city in s for s in biggest_cities):
        return 'biggest_cities'
    return 'rest'

# df_train['city_class'] = df_train['city'].apply(city_class)
