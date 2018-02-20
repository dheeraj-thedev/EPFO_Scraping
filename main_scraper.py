import requests
from shutil import copyfileobj
from captcha_reader import decode
BASE_URL = "https://unifiedportal-epfo.epfindia.gov.in"


def generate_and_read_captcha(img_src):
    my_url = BASE_URL + img_src
    response = requests.get(my_url, stream=True)
    filename = "current_captcha.png"
    with open(filename,
              "wb") as f:  # I know that "wb" and "w" do the same thing on mac, this is for universality
        copyfileobj(response.raw, f)
    del response
    return decode(filename)

