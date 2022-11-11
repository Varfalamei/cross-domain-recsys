from abc import ABC, abstractmethod

from src.structs import ItemType


class FilmsBooksStorage(ABC):
    """abstract FilmsBooksStorage 

    Args:
        ABC (_type_): _description_

    Raises:
        NotImplementedError: must to use methods
    """
    @abstractmethod
    def get_item_by_id(self, _id: int, _type: ItemType) -> dict:
        raise NotImplementedError()
