from rapidfuzz import fuzz

FUZZY_MATCH_RATIO = .8


class Book:
    def __init__(self, title: str, author: str, link: str, isbn='') -> None:
        self.title, self.link, self.isbn = clean(title), clean(link), clean(isbn)
        if ',' in author:
            last, first = clean(author).replace('*', '').split(',')
            self.author = f'{first.strip()} {last}'
        else:
            self.author = author

    def __eq__(self, other) -> bool:
        if not isinstance(other, Book):
            return False
        if self.isbn and other.isbn:
            return self.isbn == other.isbn
        else:
            return fuzz.partial_ratio(self.title, other.title) >= FUZZY_MATCH_RATIO \
                   and fuzz.partial_ratio(self.author, other.author) >= FUZZY_MATCH_RATIO

    def __str__(self) -> str:
        return f'{self.title} by {self.author} ({self.link})'

    def __repr__(self) -> str:
        return f'{self.title} by {self.author} ({self.link})'


def clean(string: str) -> str:
    return ' '.join(string.split())


def compare(goodreads_books: list[Book], amazon_books: list[Book]):
    for goodreads_book in goodreads_books:
        for amazon_book in amazon_books:
            if goodreads_book == amazon_book:
                print('This book from your list:', goodreads_book, '\n\tmight be on sale:', amazon_book)
