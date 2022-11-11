from abc import ABC, abstractmethod

from src.structs import ItemType


class FilmsBooksStorage(ABC):

    @abstractmethod
    def get_item_by_id(self, _id: int, _type: ItemType) -> dict:
        raise NotImplementedError()
