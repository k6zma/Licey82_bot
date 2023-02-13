FROM python:3.9.7

WORKDIR /home/k6zma/docker
RUN pip3 install --upgrade setuptools
RUN pip3 install aiogram==2.25.1 telegram==0.0.1
RUN chmod 755 . .
COPY . .
