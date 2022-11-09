import argparse
import time

from lemmatizer import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str)
    args = parser.parse_args()

    path = args.path
    type_ = path.split('.')[0]
    
    print(f'{path=} {type_=}')
    df = pd.read_csv(path)
    df['lemmas'] = ''
    
    l = len(df)
    for row in df.iterrows():

        i, item_row = row
        
        try:
            lemmas = GenresLemmatizer(row_to_item(item_row, type_)).get_lemmas()
        except Exception as e:
            print(i, e)
            time.sleep(3 * 60)
            
            try:
                lemmas = GenresLemmatizer(row_to_item(item_row, type_)).get_lemmas()
            except Exception as e:
                print('Double error!', i, e)
                lemmas = set()
        print(f'{i}/{l} - Success')
        df.at[i, 'lemmas'] = lemmas
        df.to_csv(f'lemmas_{type_}.csv')
