import pandas as pd
import difflib

from typing import List, Dict

from src.database.storage import FilmsBooksStorage

from src.structs import ItemType
from src.utils import string_to_set
from src.preprocessing import Preprocessor

def search(user_input: str, database: List) -> List:

    words = user_input.split()
    info_states = dict()

    for film in database:
        info_states[film] = {
            'data': film.split(),
            'counter': 0,
        }
    
    for word in words:
        for film, data in info_states.items():
            info_states[film]['counter'] += len(difflib.get_close_matches(word, data['data']))
    
    res = {k: v for k, v in sorted(info_states.items(), key=lambda item: -item[1]['counter'])}
    res = [k for k, v in res.items() if v['counter'] >= 1][0:5]
    return res


class FilmsBooksLocalStorage(FilmsBooksStorage):

    def __init__(self, books_path: str, films_path: str) -> None:
        self._books = pd.read_csv(books_path, index_col=0)
        self._books['lemmas_inter'] = self._books['lemmas_inter'].apply(lambda x: string_to_set(x))
        self._books['id'] = self._books['id'].astype(int)
                                                
        self._films = pd.read_csv(films_path, index_col=0)
        self._films['lemmas_inter'] = self._films['lemmas_inter'].apply(lambda x: string_to_set(x))
        self._films['id'] = self._films['id'].astype(int)

    def __get_replica(self, _type: ItemType) -> pd.DataFrame:
        data = None
        if _type ==  ItemType.FILM:
            data = self._films
        elif _type == ItemType.BOOK:
            data = self._books
        return data

    def get_item_by_id(self, _id: int, _type: ItemType) -> Dict:

        data = self.__get_replica(_type)
        res = data[data['id'] == _id].to_dict('list')
        for k, v in res.items():
            res[k] = v[0]
        return res

    def find_matches_by_title(self, title: str, _type: ItemType) -> List:
        data = self.__get_replica(_type)
        return search(title, data['title'].values)

    def find_id_by_title(self, title: str, _type: ItemType) -> int:
        data = self.__get_replica(_type)

        try:
            return data[data.title == title].sort_values('popularity', ascending=False).head(1)['id'].item()
        except Exception as e:
            print(e)
            return None

    def preprocess_book_by_id(self, _id: int) -> pd.DataFrame:
        return Preprocessor().create_features(
            self._books[self._books['id'] == _id], 
            self._films
        )

    def recommend(self, _id: int, model) -> List[int]:
        data = self.preprocess_book_by_id(_id)
        data['rec'] = data['accuracy']
        print(data.sort_values('rec'))
        # data['rec'] = model.predict_proba(data.drop(['book_id', 'film_id'], axis=1))[0:, 0]
        print(data.sort_values('rec').tail(5)['film_id'].values)
        return list(data.sort_values('rec').tail(5)['film_id'].values)
