from dataclasses import dataclass

import pandas as pd

import spacy
import wikipediaapi
import time

from src.structs import ItemType


nlp = spacy.load('ru_core_news_sm')
wiki = wikipediaapi.Wikipedia(language='ru', extract_format=wikipediaapi.ExtractFormat.HTML)

@dataclass
class Item:
    title: str
    genres: set
    type_: ItemType


class WikiCategorizer:
    
    def __init__(self, item: Item):
        self.item = item
        self.type = item.type_
        self.title = self._prepare_title(item.title)
    
    def _prepare_title(self, title):
        words = title.split()
        res = words[0]
        for word in words[1:]:
            res += '_' + word
        
        return res

    def get_categories(self):
        
        if self.type == ItemType.BOOK:
            titles = {self.title, self.title + '_(роман)', self.title + '_(книга)', self.title + '_(повесть)'}
            for title in titles:
                res = self._get_raw_books_categories(title)
                if not res:
                    continue
                return res
        elif self.type == ItemType.FILM:
            titles = {self.title, self.title + '_(фильм)', self.title + '_(кино)'}
            for title in titles:
                res = self._get_raw_books_categories(title)
                if not res:
                    continue
                return res
        return set()

    def _get_raw_films_categories(self, wiki_url: str) -> set:

        wiki = wikipediaapi.Wikipedia(language='ru', extract_format=wikipediaapi.ExtractFormat.HTML)
        p = wiki.page(wiki_url)

        elems = set()
        for k, v in p.categories.items():
            elem = k.split(':')[1]

            if 'фильмы' in elem.lower():
                elems.add(elem)

        return elems

    def _get_raw_books_categories(self, wiki_url: str) -> set:

        wiki = wikipediaapi.Wikipedia(language='ru', extract_format=wikipediaapi.ExtractFormat.HTML)
        p = wiki.page(wiki_url)

        elems = set()
        for k, v in p.categories.items():
            elem = k.split(':')[1]

            if 'книги' in elem.lower() or\
            'фильмы' in elem.lower() or\
            'романы' in elem.lower() or\
            'произведения' in elem.lower() or\
            'повести' in elem.lower():
                elems.add(elem)

        return elems
    

class GenresLemmatizer(WikiCategorizer):

    def get_lemmas(self):
        return get_spacy_lemmas(self.get_categories().union(self.item.genres))


def row_to_item(row, type_: str) -> Item:

    return Item(
        title=row['title'],
        genres=set(row['genres'].split(',')),
        type_=ItemType(type_)
    )

def apply_lemmatizer(row):
    item = row_to_item(row, 'film')
    
    try:
        lemmas = GenresLemmatizer(item).get_lemmas()
    except Exception as e:
        print(e)
        time.sleep(3 * 60)
        lemmas = GenresLemmatizer(item).get_lemmas()
    return lemmas

