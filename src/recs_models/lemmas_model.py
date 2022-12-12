from typing import List

from src.recs_models.base_model import BaseModel
from src.database.local_storage import FilmsBooksLocalStorage
from src.structs import ItemType


class LemmasModel(BaseModel):
    """Lemmas recommedner

    Args:
        BaseModel: Model interface
    """
    def __init__(self, db: FilmsBooksLocalStorage) -> None:
        self._db = db

    def recommend(self, book_id: int, k: int = 5) -> List[int]:
        """recommend algorithm

        Args:
            _id (int): book id
            model (_type_): model with predict_proba method

        Returns:
            List[int]: recommendations [id]
        """
        book = self._db.get_item_by_id(book_id, _type=ItemType.BOOK)
        if book['lemmas_inter'] == set():
            return []
        data = self._db.get_replica(ItemType.FILM)
        data['rec'] = data['lemmas_inter'].apply(
            lambda x: 
            len(book['lemmas_inter'].intersection(x))/\
                (len(book['lemmas_inter']) + 3 * len(x))
        )
        print(book['lemmas_inter'])
        print(data.sort_values(['rec', 'popularity'], ascending=False).head(k)[['title', 'rec', 'lemmas_inter', 'popularity']])
        return list(data.sort_values(['rec', 'popularity'], ascending=False).head(k)['id'].values)
