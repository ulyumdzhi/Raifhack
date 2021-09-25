def region_replacer(region: str) -> str:
        """
        Приводим названия регионов к общему виду
        """
        region = region.replace('Г. ', '').replace('Республика ', '').strip()
        rep = {'Удмуртская Республика': 'Удмуртия', 'Ханты-Мансийский автономный округ — Югра':'Ханты-Мансийский АО'}
        if region in rep:
            region = rep[region]
        
        return region