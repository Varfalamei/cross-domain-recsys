import string
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import scipy

warnings.filterwarnings("ignore")


def rec_to_excel(
    target_books_df, films_df, text_transformer, top_k=5, top_k_w=10, filename="rec"
) -> pd.DataFrame:
    """
    Функция, которая заносит рекомендуемые фильмы в эксель файл

    Input:
        target_books_df: pd.DataFrame датасет с целевыми книгами
        films_df: pd.DataFrame датасет с фильмами, которые будут рекомендоваться
        text_transformer: объект с методами .transform и  .inverse_transform, которые переводят текст в числовой вектор и наоборот
        top_k: int топ рекомендаций
        top_k_w: int кол-во слов, которые отобразятся в пересечении
        filename: str имя файла

    Return:
        pd.DataFrame датафрейм с рекомендациями

    """
    t_books_sparce = text_transformer.transform(target_books_df["annotation"])
    films_sparce = text_transformer.transform(films_df["description"])
    similarity = cosine_similarity(t_books_sparce, films_sparce)

    similarity_id = np.argsort(-similarity)
    similarity = -np.sort(-similarity)
    top_films_id = similarity_id[:, :top_k]
    top_films_sim = similarity[:, :top_k]

    top_words = [[] for i in range(t_books_sparce.shape[0])]
    for i in range(t_books_sparce.shape[0]):
        for j in range(top_k):
            temp = list(
                zip(
                    *scipy.sparse.find(
                        t_books_sparce[i].multiply(films_sparce[top_films_id[i][j]])
                    )[1:]
                )
            )
            temp.sort(key=lambda x: x[1], reverse=True)
            temp = [temp[i][0] for i in range(min(len(temp), top_k_w))]
            zeros = np.zeros(t_books_sparce.shape[1])
            zeros[[temp]] = 1
            words = text_transformer.inverse_transform(zeros.reshape(1, -1))[0].tolist()
            top_words[i].append(words)

    res = {
        "book_title": [],
        "book_genre": [],
        "film_title": [],
        "film_genre": [],
        "similarity": [],
        "top_words": [],
    }
    for i in range(len(top_films_id)):
        for j in range(top_k):
            res["book_title"].append(target_books_df["title"].iloc[i])
            res["book_genre"].append(target_books_df["genres"].iloc[i])
            res["film_title"].append(films_df.iloc[top_films_id[i][j]]["title"])
            res["film_genre"].append(films_df.iloc[top_films_id[i][j]]["genres"])
            res["similarity"].append(top_films_sim[i][j])
            res["top_words"].append(top_words[i][j])

    temp_df = pd.DataFrame(res)
    temp_grouped = temp_df.groupby(
        by=["book_title", "book_genre", "film_title", "film_genre"], sort=False
    ).first()

    def save_excel_with_optimized_col_width(df, filename, index: bool):
        writer = pd.ExcelWriter(filename)
        df.to_excel(writer, index=index, sheet_name="Sheet")
        worksheet = writer.sheets["Sheet"]
        if index:
            df_ = df.reset_index()
        else:
            df_ = df
        for idx, col in enumerate(df_):
            lenghts = pd.Series(df_[col].astype(str).str.len().tolist() + [len(col)])
            max_len = lenghts.max()
            if max_len < 50:
                width = max_len + 1
            else:
                width = min(lenghts.quantile(0.8), 100)
            col_letter = string.ascii_uppercase[idx]
            worksheet.set_column(idx, idx, width)
        writer.save()

    save_excel_with_optimized_col_width(temp_grouped, f"{filename}.xlsx", index=True)

    return temp_grouped
