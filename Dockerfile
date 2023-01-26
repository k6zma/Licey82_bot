FROM python:3.9.7

WORKDIR /home/k6zma/docker
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade setuptools
RUN pip3 install requirements.txt
RUN chmod 755 . .
COPY . .
