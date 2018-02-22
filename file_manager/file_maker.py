from unidecode import unidecode


def write_new_table(company, code, month, year, name_list):
    with open("stored_tables/"+company+"_"+code+"_"+month+"_"+year+".txt", "w") as f:
        for name in name_list:
            f.write(unidecode(name)+"\n")