def sort_prods(filter_cake: list[int | dict]):
    def wrapper(prods: tuple[int | list[int | dict]]):
        score = 0

        type_filter = filter_cake[0]
        ingrs_tastes_filter = filter_cake[1]
        ingrs_filter = ingrs_tastes_filter.keys()

        type_check = prods[1][0]
        ingrs_check = prods[1][1]

        if type_filter == type_check:
            score += 100

        if ingrs_check == ingrs_tastes_filter:
            return (-1000, prods[0])
        
        for ingr, tastes in ingrs_check.items():
            if ingr in ingrs_filter:
                score += len(set([tastes]) & set(ingrs_tastes_filter[ingr])) #! Не забыть заменить [tastes] на список в бд

        return (-score, prods[0][0])
    
    return wrapper