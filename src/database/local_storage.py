import pandas as pd
import difflib

from typing import List, Dict

from src.database.storage import FilmsBooksStorage

from src.structs import ItemType
from src.utils import string_to_set
from src.preprocessing import Preprocessor


def search(user_input: str, database: List) -> List:
    """Simple search engine to find user_input
    title in list of title in database

    Args:
        user_input (str): user request to search
        database (List): database with results

    Returns:
        List: list of the best matches
    """
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
    """FilmsBooksLocalStorage

    Args:
        FilmsBooksStorage: ABC
    """

    def __init__(self, books_path: str, films_path: str) -> None:
        """

        Args:
            books_path (str): books db
            films_path (str): films_path db
        """
        self._books = pd.read_csv(books_path, index_col=0)
        self._books['lemmas_inter'] = self._books['lemmas_inter'].apply(lambda x: string_to_set(x))
        self._books['id'] = self._books['id'].astype(int)
                                                
        self._films = pd.read_csv(films_path, index_col=0)
        self._films['lemmas_inter'] = self._films['lemmas_inter'].apply(lambda x: string_to_set(x))
        self._films['id'] = self._films['id'].astype(int)

    def get_replica(self, _type: ItemType) -> pd.DataFrame:
        """Return exact dataframe by ItemType

        Args:
            _type (ItemType): film/book

        Returns:
            pd.DataFrame: replica of inner df
        """
        data = None
        if _type ==  ItemType.FILM:
            data = self._films
        elif _type == ItemType.BOOK:
            data = self._books
        return data

    def get_item_by_id(self, _id: int, _type: ItemType) -> Dict:
        """get_item_by_id

        Args:
            _id (int): item id
            _type (ItemType): item type

        Returns:
            Dict: info from db
        """

        data = self.get_replica(_type)
        res = data[data['id'] == _id].to_dict('list')
        for k, v in res.items():
            res[k] = v[0]
        return res

    def find_matches_by_title(self, title: str, _type: ItemType) -> List:
        """find_matches_by_title

        Args:
            title (str): item title
            _type (ItemType): item type

        Returns:
            List: return best matches using searching engine
        """
        data = self.get_replica(_type)
        return search(title, data['title'].values)

    def find_id_by_title(self, title: str, _type: ItemType) -> int:
        """find_id_by_title

        Args:
            title (str): item title
            _type (ItemType): item type

        Returns:
            int: item id in db
        """
        data = self.get_replica(_type)

        try:
            print(title)
            return data[data.title == title].sort_values('popularity', ascending=False).head(1)['id'].item()
        except Exception as e:
            print(e)
            return None

    def preprocess_book_by_id(self, _id: int) -> pd.DataFrame:
        """preprocess_book_by_id

        Args:
            _id (int): book_id

        Returns:
            pd.DataFrame: generated featues
        """
        return Preprocessor().create_features(
            self._books[self._books['id'] == _id], 
            self._films
        )
