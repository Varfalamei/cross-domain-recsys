from typing import Dict, List
import pandas as pd

def IoU(films_rec: list, films_match: list):
    films_rec = set(films_rec)
    films_match = set(films_match)
    intersection = films_rec.intersection(films_match)
    max_length = max(len(films_rec), len(films_match))

    return len(intersection) / max_length


def metric_film_adaptations(
    recommendations: pd.DataFrame,
    matching: pd.DataFrame
) -> float:
    """
    This metric is calculated based on movie recommendations based on books.
    We want to know if we have a movie adaptation of the book in our recommendation.

    How to calculate:
      If there is a film adaptation of the book, we put a match, otherwise there 
      is no match. If there aren't any film adaptations we add 0.5 to result.
      Next, we average the result

    Explanation of the metric:
      This metric like a roc_auc. If metric > 0.5, it is good, otherwise it is bad XD

    Input:
      recommendations: Dataframe with book id as a key and movie ids as value
      matching: Dataframe that contains a book id and a movie id.
                Has to have 'id_book' and 'id_film' columns

    Return:
      metric value
    """

    assert 'book_id' in set(recommendations.columns) and \
      'film_id' in set(recommendations.columns) and \
      'book_id' in set(matching.columns) and \
      'film_id' in set(matching.columns), \
      "matching doesn't contain right columns, please rename them to id_film and id_book"

    matching = (
        matching
        .groupby(['book_id'])['film_id']
        .apply(list)
        .reset_index(name='film_id')
    )
    recommendations = (
        recommendations
        .groupby(['book_id'])['film_id']
        .apply(list)
        .reset_index(name='film_id')
    )
    

    book_intersection = recommendations.merge(
        matching, on='book_id', how='inner', suffixes=('_rec', '_match')
    )

    print('intersection of datasets is - ', len(book_intersection))

    book_intersection = book_intersection.apply(lambda x: IoU(x['film_id_rec'], x['film_id_match']), axis=1)
    result = sum(book_intersection) / book_intersection.shape[0]

    return result