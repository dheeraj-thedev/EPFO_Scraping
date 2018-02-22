"""
Use this after you have already downloaded the tables for the company.
"""

from os import listdir
from misc.month_payment_sorter import sort_month_and_payment


def find_employee(employee, company):
    univ_dict = get_last_three_month_dictionary(company)



def get_last_three_month_dictionary(company):
    my_dict = dict()
    for filename in listdir("stored_tables/"+company+"/"):
        if filename.startswith(company):
            lol = filename.split(".")
            my_list = lol[0].split("_")
            if my_list[1] in my_dict.keys():
                my_dict[my_list[1]].append((my_list[3], my_list[2], filename))
            else:
                my_dict[my_list[1]] = [(my_list[3], my_list[2], filename)]
    for key in my_dict:
        sorted_list = sort_month_and_payment(my_dict[key])[-3:]
        my_dict[key] = sorted_list
    return my_dict
