import re

from .constants_and_types import PRICE_WEIGHTS

class Item:
    def __init__(self, name: str, price: str, descr: str, url: str, categories: list):
        clean_descr = lambda s: re.sub(r'^[«"<]+|[»">]+$', '', s)
        self.name: str = name
        self.price: str = price
        self.price_weight: int = PRICE_WEIGHTS[self.price]
        self.descr: str = clean_descr(descr.strip()).strip()
        self.url: str = url
        self.categories: list = categories

    def get_main_category(self) -> str:
        return self.categories[0]

    def __str__(self) -> str:
        categories = " | ".join(self.categories)
        return f'| [{self.name}]({self.url}) | {self.price} | {self.descr} | {categories} |'
    