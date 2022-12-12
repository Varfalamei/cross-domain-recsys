import os

from src.database import FilmsBooksLocalStorage
from src.recs_models.lemmas_model import LemmasModel


books_path = os.getenv('BOOKS_PATH', '/src/books_with_lemmas.csv')
films_path = os.getenv('FILMS_PATH', '/src/books_with_lemmas.csv')

db = FilmsBooksLocalStorage(
    books_path=books_path,
    films_path=films_path
)

MODELS = {
    'lemmas': LemmasModel(db),
}

DEFAULT_MODEL = 'lemmas'
