
month_to_num_map = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6, "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12}


def get_month_number(month):
    return month_to_num_map[month]


def month_sort(month_1, month_2):
    m1 = get_month_number(month_1); m2 = get_month_number(month_2)
    if m1 > m2:
        return 1
    if m1 < m2:
        return -1
    if m1 == m2:
        return 0

# def


# print(month_sort("JAN", "FEB"))