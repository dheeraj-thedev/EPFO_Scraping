import requests
from shutil import copyfileobj
from bs4 import BeautifulSoup as soup
from captcha_reader import decode
import json
INITIAL_URL = "https://unifiedportal-epfo.epfindia.gov.in/publicPortal/no-auth/misReport/home/loadEstSearchHome/"


def generate_and_read_captcha(my_soup, session):
    img_src = my_soup.find("div", {"id": "captchaImg"}).find("img")['src']
    my_url = get_full_url(img_src)
    response = session.get(my_url, stream=True)
    filename = "current_captcha.png"
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
    if name_list:
        print("There are", len(name_list), "companies registered with the given name. "
                                           "Following are their ID numbers.")
        print(name_list)
    return name_list


def prompt_company():
    return input("Which company do you want to search for? The name isn't case sensitive.\n")


def prompt_employee_name():
    return input("What is the required employee's name?\n")


def which_index():
    return input("Which of the companies (0-indexed) would you like to check?\n")


def post_get_company_details(r, session, company_code):
    my_soup = soup(r.text, "html.parser")
    my_url = get_full_url(my_soup.find_all("a", href=True)[0]["onclick"].split(",'")[1][:-1])
    print(my_url)
    response = session.post(my_url, data=json.dumps({"EstId": company_code}), headers={'Content-Type': 'application/json'})
    # print(response.text)
    return response



def main():
    pass


if __name__ == '__main__':
    s = requests.Session()
    my_soup = get_soup(s, INITIAL_URL)
    company_list = []
    # company = prompt_company()
    while not company_list:  # in case the captcha reader fails
        # r = post_search_establishment_request(my_soup, s, company)
        r = post_search_establishment_request(my_soup, s, "google")
        company_list = get_company_list(r)
    # employee = prompt_employee_name()
    # code = None
    # while code is None:
    #     try:
    #         code = company_list[int(which_index())]
    #     except IndexError:
    #         print("Your index was out of bounds. Enter a proper one, under", str(len(company_list)), ".")
    code = company_list[0]
    company_details = post_get_company_details(r, s, code)

