from typing import Dict, List
import pandas as pd

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
    book_ids = list(recommendations.book_id.unique())
    result = 0

    for book_id in book_ids:
        film_recs = recommendations[recommendations.book_id == book_id].film_id.tolist()
        film_adaptations = matching[matching.book_id == book_id].film_id.tolist()
        if film_adaptations:
            if set(film_adaptations).intersection(set(film_recs)) != set():
                result += 1
            else:
                result += 0
        else:
            result += 0.5

    return round(result / len(book_ids), 4)
