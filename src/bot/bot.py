import sklearn
import pickle
import os
import warnings

from src.database import FilmsBooksLocalStorage
from src.structs import ItemType


warnings.filterwarnings("ignore")


if __name__ == '__main__':

    model_path = os.getenv('MODEL_PATH')
    books_path = os.getenv('BOOKS_PATH')
    films_path = os.getenv('FILMS_PATH')

    with open(model_path, 'rb') as file:
        model = pickle.load(file)
        
    db = FilmsBooksLocalStorage(
        books_path=books_path,
        films_path=films_path
    )

    print('Введите название книги:\n>', end='')
    book_title = input()
    titles = db.find_matches_by_title(book_title, ItemType.BOOK)

    print('Выберите книгу\n')
    for i, title in enumerate(titles):
        print(f'({i+1}) - {title}')

    print('>', end='')
    id_ = int(input())
    book_id = db.find_id_by_title(titles[id_-1], ItemType.BOOK)

    recs = db.recommend(book_id, model)

    for i, rec in enumerate(recs):
        item = db.get_item_by_id(rec, ItemType.FILM)
        print(f'({i}) - {item["title"]}, {item["year"]}, {", ".join(item["lemmas_inter"])}')
