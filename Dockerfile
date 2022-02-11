FROM nikolaik/python-nodejs:latest

ADD . .

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip  install -e .
RUN pip install pytest

WORKDIR /tests/

CMD ["pytest"]