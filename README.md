# cross-domain-recsys
Cross-Domain recommender system to recommend books based on movies and movies based on books


## How to run bot

```
docker build -t bot
docker run -e "BOT_TOKEN=12345" -d bot
```

Bot: https://t.me/books_rec_bot


## How to add new model
1. Add new `class` to `src/recs_models` which implemets `BaseModel` inteface:

```
from typing import List
from abc import ABC, abstractmethod


class BaseModel(ABC):

    @abstractmethod
    def recommend(self, book_id: int, k: int = 5) -> List[int]:
        """recommend algorithm

        Args:
            _id (int): book id
            k (int): size of recs

        Returns:
            List[int]: recommendations [id]
        """
        raise NotImplementedError

```

The example of online model that uses FilmsBooksLocalStorage:

```
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
```
2. Update `src/bot/meta.py`:
```
from src.recs_models.my_new_model import MyNewModel

MODELS = {
    'my_new_model': LemmasModel('/src/models/my_new_model.bin'),
}
```
Than you can set this model to defualt on bot or switch it using 
