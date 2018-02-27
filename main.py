from epfo_scraper import make_last_n_tables_for_company, get_comp_list
from misc.prompts import prompt_company, which_index, prompt_employee_name
from fuzzywuzzy import process

def perform_scrape():
    name = prompt_company()
    comp_list = get_comp_list(name)
    print("Following are the companies which were found under your search.")
    print(comp_list[0])
    return make_last_n_tables_for_company(name, int(which_index()))


def find_employee(name_dict, name, fuzzy=True):
    present_dict = dict()
    for company in name_dict:
        l = company.split("_")
        if fuzzy:
            present_dict[l[1]] = process.extract(name, name_dict[company], limit=5)
        else:
            if name.upper() in name_dict[company]:
                present_dict[l[1]] = True
            else:
                present_dict[l[1]] = False

    return present_dict


if __name__ == '__main__':
    company = perform_scrape()
    while True:
        print(find_employee(company, prompt_employee_name()))





