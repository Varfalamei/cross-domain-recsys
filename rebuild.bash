docker stop BOT
docker build . -t bot
docker run -e "BOT_TOKEN=" --name=BOT
