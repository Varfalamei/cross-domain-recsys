FROM python:3.8

WORKDIR /src

COPY /src /src/

COPY /data /src/

RUN pip3 install -r requirements.txt

ENV PYTHONPATH /

CMD [ "python3", "bot/bot.py" ]

