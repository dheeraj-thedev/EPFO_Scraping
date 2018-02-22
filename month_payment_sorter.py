
month_to_num_map = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6, "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12}


def get_month_number(month):
    return month_to_num_map[month]


def sort_month_and_payment(tuple_list):
    return sorted(tuple_list, key=lambda y: (y[0], get_month_number(y[1])))
