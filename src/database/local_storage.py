from database.storage import FilmsBooksStorage

from src.structs import ItemType
from src.utils import string_to_set


class FilmsBooksLocalStorage(FilmsBooksStorage):


    def __init__(self, books_path: str, films_path: str) -> None:
        self._books = pd.read_csv(books_path, index_col=0)
        self._books['lemmas_inter'] = self._books['lemmas_inter'].apply(lambda x: string_to_set(x))
                                                                        
        self._films = pd.read_csv(films_path, index_col=0)
        self._films['lemmas_inter'] = self._films['lemmas_inter'].apply(lambda x: string_to_set(x))


    def get_item_by_id(self, _id: int, _type: ItemType) -> dict:

        data = None
        if ItemType(_type) ==  ItemType.FILM:
            data = self._films
        elif ItemType(_type) == ItemType.BOOK:
            data = self._books

        res = data[data['id'] == _id].to_dict('list')
        for k, v in res.items():
            res[k] = v[0]
        return res
