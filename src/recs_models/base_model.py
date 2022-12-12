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
