FROM nikolaik/python-nodejs:python3.7-nodejs6

ADD . .

RUN pip3 install --upgrade pip
RUN pip3  install -e .
RUN pip3 install pytest

WORKDIR /tests/

CMD ["pytest", "-x"]