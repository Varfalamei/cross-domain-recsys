class Metrics:
    def __init__(self, gold_rec, new_rec):
        self.gold_rec = gold_rec[["book_title", "film_title", "rank"]]
        self.new_rec = new_rec[["book_title", "film_title"]]

    def metric_set(self):
        ans = {"book_title": [], "similarity": []}

        gr_gold = self.gold_rec.groupby(by=["book_title"], sort=False)[
            "film_title"
        ].agg(size=len, set=lambda x: set(x))
        gr_gold["book_title"] = gr_gold.index
        gr_new = self.new_rec.groupby(by=["book_title"], sort=False)["film_title"].agg(
            size=len, set=lambda x: set(x)
        )
        gr_new["book_title"] = gr_new.index

        books_list = gr_new["book_title"].tolist()
        for i in range(len(books_list)):

            book = books_list[i]
            new_data = gr_new[gr_new["book_title"] == book][["size", "set"]].values[0]
            try:
                gold_data = gr_gold[gr_gold["book_title"] == book][
                    ["size", "set"]
                ].values[0]
            except IndexError:
                ans["book_title"].append(book)
                ans["similarity"].append("-")
                continue

            similarity = len(gold_data[1] & new_data[1]) / gold_data[0]
            ans["book_title"].append(book)
            ans["similarity"].append(similarity)

        return pd.DataFrame(ans)

    def metric2(self):
        pass
