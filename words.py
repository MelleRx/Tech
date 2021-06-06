def correct_word(counter):
    if counter % 10 == 1 and counter % 100 != 11:
        return " блюдо"
    elif counter % 10 == 2 and counter % 100 != 12 or counter % 10 == 3 and counter % 100 != 13 or counter % 10 == 4 \
            and counter % 100 != 14:
        return " блюда"
    else:
        return " блюд"


