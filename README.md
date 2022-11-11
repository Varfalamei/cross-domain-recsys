# cross-domain-recsys
Cross-Domain recommender system to recommend books based on movies and movies based on books

## Installation

``` shell
# apt install required packages:
sudo apt update
sudo apt install -y zip htop pipenv
  
# clone repo:
git clone https://github.com/Varfalamei/cross-domain-recsys.git
# go to the folder:
cd cross-domain-recsys

```


## Main contributors

Product owner: [Эмиль](https://github.com/feldlime) 

1. [Шакиров Ренат](https://github.com/Varfalamei)
2. [Крестенко Анатолий](https://github.com/likeblood)

``` shell
# For contributing please use linterts and hooks the following commands:
black .
pre-commit run --all-files
 ```

## How to run bot

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

export MODEL_PATH=/path/to/model
export BOOKS_PATH=/path/to/books
export FILMS_PATH=/path/to/films
export PYTHONPATH=/path/to/project

python3 bot.py
```