FROM nikolaik/python-nodejs:latest

ADD . .

RUN pip3 install --upgrade pip
RUN pip3  install -e .
RUN pip3 install pytest

WORKDIR /tests/

CMD ["pytest"]