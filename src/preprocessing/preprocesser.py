import pandas as pd


class Preprocessor:
    """Preprocessor
    """
    def create_features(self, books: pd.DataFrame, films: pd.DataFrame) -> pd.DataFrame:
        """Generate data by frames

        Args:
            books (pd.DataFrame): books db
            films (pd.DataFrame): films db

        Returns:
            pd.DataFrame: featured df with books X films size
        """
        
        books['key'] = 0
        films['key'] = 0

        df = books.merge(films, on='key', how='outer')
        df = df[['id_x', 'id_y', 'lemmas_inter_x', 'lemmas_inter_y']]
        df.columns = ['book_id', 'film_id', 'book_lemmas', 'film_lemmas']

        df['accuracy'] = df.apply(lambda row: len(row['film_lemmas'].intersection(row['book_lemmas'])) / len(row['book_lemmas']), axis=1)
        for book_weight, film_weight in ([1, 0], [1, 2], [1, 3],
                [0, 1], [2, 1], [3,1],
                [1, 1]):
            df[f'waccuracy_{book_weight}_{film_weight}'] =\
                df.apply(lambda row: len(row['film_lemmas'].intersection(row['book_lemmas'])) /\
                (book_weight*len(row['book_lemmas']) + film_weight*len(row['film_lemmas'])), axis=1)
        
        for l in range(3):
            df[f'absaccuracy_{l}'] =\
                df.apply(lambda row: (len(row['film_lemmas'].intersection(row['book_lemmas'])) - l*len(row['book_lemmas'])) / len(row['book_lemmas']), axis=1)
        
        df['len_book_lemmas'] = df['book_lemmas'].apply(lambda x: len(x))
        df['len_films_lemmas'] = df['film_lemmas'].apply(lambda x: len(x))
        df['len_intersection'] = df.apply(lambda row: len(row['film_lemmas'].intersection(row['book_lemmas'])), axis=1)

        return df.drop(['book_lemmas', 'film_lemmas'], axis=1)
