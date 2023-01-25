FROM python:3.9.7

WORKDIR /TelegramBots
ENV TELEGRAM_API_TOKEN="5797613512:AAEA_X53UFFWyg6qfnWBhQtWS0rHJwovEmU"


RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
RUN apt-get install sqllite3
COPY . .

ENTRYPOINT ["python", "bot_telegram.py"]