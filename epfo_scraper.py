import requests
from bs4 import BeautifulSoup as soup
from misc.captcha_reader import decode
import json
from misc import month_payment_sorter
from file_manager import file_maker as fm

INITIAL_URL = "https://unifiedportal-epfo.epfindia.gov.in/publicPortal/no-auth/misReport/home/loadEstSearchHome/"


def generate_and_read_captcha(my_soup, session):
    img_src = my_soup.find("div", {"id": "captchaImg"}).find("img")['src']
    my_url = get_full_url(img_src)
    response = session.get(my_url, stream=True)
    filename = "misc/current_captcha.png"
    with open(filename,
              "wb") as f:  # I know that "wb" and "w" do the same thing on mac, this is for universality
        f.write(response.content)
    del response
    return decode(filename)


def get_full_url(sub_url):
    base_url = "https://unifiedportal-epfo.epfindia.gov.in"
    return base_url+sub_url


def get_soup(session, url):
    response = session.get(url)
    my_soup = soup(response.text, "html.parser")
    return my_soup


def post_search_establishment_request(my_soup, session, est_name, est_code=""):
    est_req = my_soup.find("div", {"class": "col-sm-3 col-md-2 col-lg-2"}).input['onclick'].split("'")[1]
    my_url = get_full_url(est_req)
    response = None
    # print(session.cookies)
    while response is None:
        captcha = generate_and_read_captcha(my_soup, session)
        response = session.post(my_url, data=json.dumps({"EstName": est_name, "EstCode": est_code, "captcha": captcha}),
                                headers={'Content-Type': 'application/json'})
    return response


def get_company_list(establishment_response):
    my_soup = soup(establishment_response.text, "html.parser")
    name_list = []
    for org in my_soup.find_all("a", href=True):
        name_list.append(org["name"])
    # if name_list:
        # print("There are", len(name_list), "companies registered with the given name. "
        #                                    "Following are their ID numbers.")
        # print(name_list)
    return name_list


def post_get_company_details(r, session, company_code):
    my_soup = soup(r.text, "html.parser")
    my_url = get_full_url(my_soup.find_all("a", href=True)[0]["onclick"].split(",'")[1][:-1])
    # print(my_url)
    response = session.post(my_url, data=json.dumps({"EstId": company_code}), headers={'Content-Type': 'application/json'})
    return response


def view_payment_details(details, session):
    detail_soup = soup(details.text, "html.parser")
    # print(detail_soup)
    my_url = get_full_url(detail_soup.find("a", href=True)["onclick"].split("'")[1])
    payment = session.get(my_url)
    return payment


def get_last_three_months_payment(payment_details):
    payment_soup = soup(payment_details.text, "html.parser")
    # the data here is stored in a pretty ugly way, need to sort
    parsed_list = []
    for row in payment_soup.find_all("tr")[1:]:  # first row is the title row
        date = row.find_all("td")[3].find(text=True).split("-")
        pay_link = row.find("a", href=True)["onclick"].split("'")[1]
        my_trrn = row.find_all("td")[0].find(text=True)
        if int(row.find("a", href=True).contents[0]) > 5:
            parsed_list.append((date[1], date[0], pay_link, my_trrn))
    return month_payment_sorter.sort_month_and_payment(parsed_list)[-3:]


def get_payment_table(session, link, trrn):
    my_url = get_full_url(link)
    table = session.post(my_url, data=json.dumps({"Trrn": trrn}), headers={'Content-Type': 'application/json'})
    return table


def get_name_list(payment_table):
    table_soup = soup(payment_table.text, "html.parser")
    name_list = []
    for row in table_soup.find_all("tr")[1:]:  # first line is title line
        name_list.append((row.find("td").find(text=True)))
    return name_list


def get_len_of_comp_list(company_name):
    sesh = requests.Session()
    my_soup = get_soup(sesh, INITIAL_URL)
    company_list = []
    while not company_list:  # in case the captcha reader fails
        r = post_search_establishment_request(my_soup, sesh, company_name)
        company_list = get_company_list(r)
    return len(company_list)


def make_last_three_tables_for_company(company_name):
    length = get_len_of_comp_list(company_name)
    for i in range(0, length):
        sesh = requests.Session()  # have to make a new session every single time or else the prog fails
        my_soup = get_soup(sesh, INITIAL_URL)
        company_list = []
        while not company_list:  # in case the captcha reader fails
            r = post_search_establishment_request(my_soup, sesh, company_name)
            company_list = get_company_list(r)
        code = company_list[i]
        company_details = post_get_company_details(r, sesh, code)
        payment_details = view_payment_details(company_details, sesh)
        for req_payment in get_last_three_months_payment(payment_details):
            month = req_payment[1]
            year = req_payment[0]
            payment_table = get_payment_table(sesh, req_payment[2], req_payment[3])
            name_list = get_name_list(payment_table)
            fm.write_new_table(company_name, code, month, year, name_list)
