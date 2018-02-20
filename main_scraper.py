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
    print(my_url)
    response = None
    count = 0
    while response is None:
        count += 1
        print(count)
        captcha = generate_and_read_captcha(my_soup, session)
        print(captcha)
        response = session.post(my_url, data=json.dumps({"EstName": est_name, "EstCode": est_code, "captcha": captcha}))
        print(response.text)
    return response


def main():
    pass


if __name__ == '__main__':
    s = requests.Session()
    my_soup = get_soup(s, INITIAL_URL)
    print(s.cookies)
    r = post_search_establishment_request(my_soup, s, "google")