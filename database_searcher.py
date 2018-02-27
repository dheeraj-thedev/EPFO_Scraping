"""
Use this after you have already downloaded the tables for the company.
"""

from os import listdir
from misc.month_payment_sorter import sort_month_and_payment


def find_employee(employee, company, cache=True):
    if cache:
        univ_dict = get_last_three_month_dictionary(company)
    else:
        univ_dict = get_last_three_month_dictionary(company, cache=False)
    original_len = len(univ_dict)
    while True:
        print("There are", len(univ_dict), "companies to look through.")
        print("They are:", univ_dict.keys())
        if len(univ_dict) < original_len:
            need = ""
            while need != "n" and need != "y":
                need = input("Would you like to continue? Type y or n.")
            if need == "n":
                break
            print("There are", len(univ_dict), "companies to look through.")
            print("They are:", univ_dict.keys())
            inp = input("Which company would you like to search through?")
            current = univ_dict[inp]
            univ_dict.pop(inp)
            for triplet in current:
                with open(triplet[2], "r") as f:
                    for line in f:
                        if line.lower() == employee.lower():
                            print(triplet[2], "found")
            print("Sorry, we could not find the employee in", inp)
        inp = input("Which company would you like to search through?\n")
        current = univ_dict[inp]
        univ_dict.pop(inp)
        for triplet in current:
            with open(triplet[2], "r") as f:
                for line in f:
                    if line.lower().strip() == employee.lower():
                        print(triplet[2], "found")
        print("Sorry, we could not find the employee in", inp)




def get_last_three_month_dictionary(company, cache=True):
    my_dict = dict()
    for filename in listdir("stored_tables/"+company+"/"):
        if filename.startswith(company):
            lol = filename.split(".")
            my_list = lol[0].split("_")
            if my_list[1] in my_dict.keys():
                my_dict[my_list[1]].append((my_list[3], my_list[2], "stored_tables/"+company+"/"+filename))
            else:
                my_dict[my_list[1]] = [(my_list[3], my_list[2], "stored_tables/"+company+"/"+filename)]
    for key in my_dict:
        sorted_list = sort_month_and_payment(my_dict[key])[-3:]
        my_dict[key] = sorted_list
    return my_dict


find_employee("AANCHAL JAIN", "google")