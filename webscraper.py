"""
Scrapes a Goodreads book list and Kindle book list and compares them to find books on sale.
"""
import os

import requests as req
from bs4 import BeautifulSoup as soup

from helpers.book import Book, compare
from helpers import spoof

GOODREADS_URL = os.environ['GOODREADS_URL']
AMAZON_URLS = {
    'MONTHLY_DEALS': os.environ['AMAZON_MONTHLY_DEALS_URL'],
    'LIMITED_TIME_DEALS': os.environ['AMAZON_LIMITED_TIME_DEALS_URL'],
}


def scrape_goodreads() -> list[Book]:
    goodreads_books = []
    page_count = 1
    while True:
        page = soup(req.get(f'{GOODREADS_URL}&page={page_count}').content, 'html.parser')
        books = page.find_all('tr', class_='bookalike review')
        if len(books) == 0:
            break
        for book in books:
            title = book.find('td', class_='field title').find('div', class_='value').text
            author = book.find('td', class_='field author').find('div', class_='value').text
            isbn = book.find('td', class_='field isbn').find('div', class_='value').text
            link = ''  # TODO
            goodreads_books.append(Book(title, author, link, isbn))
        page_count += 1
    return goodreads_books


def scrape_amazon() -> list[Book]:
    amazon_books = []
    for URL in AMAZON_URLS:
        page_count = 1
        while True:
            page = soup(spoof.get(f'{AMAZON_URLS[URL]}&page={page_count}').content, 'html.parser')
            books = page.find_all('div', attrs={'data-component-type': 's-search-result'})
            if len(books) == 0:
                break
            for book in books:
                title = book.find('span', class_='a-size-medium a-color-base a-text-normal').text
                author = book.find('a', class_='a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style').text
                link = ''  # TODO
                amazon_books.append(Book(title, author, link))
            page_count += 1
    return amazon_books


def main():
    goodreads_books = scrape_goodreads()
    amazon_books = scrape_amazon()
    compare(goodreads_books, amazon_books)


if __name__ == "__main__":
    main()
