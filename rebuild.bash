#!/bin/bash

docker stop BOT
docker rm BOT
docker build . -t bot
docker run --name BOT -e "BOT_TOKEN=" -d bot
