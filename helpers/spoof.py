import requests as req
from bs4 import BeautifulSoup as soup
from fake_useragent import UserAgent


def get(url: str):
    ua = UserAgent()
    random_user = ua.random
    while True:
        res = req.get(url, headers={'User-Agent': random_user, 'Accept-Language': 'en-US,en;q=0.9'})
        page = soup(res.content, 'html.parser')
        if 'captcha' in str(page):
            random_user = ua.random
        else:
            return page
