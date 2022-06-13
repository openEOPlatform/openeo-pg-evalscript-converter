FROM python:3.8.13

ADD . .

SHELL ["/bin/bash", "--login", "-c"]

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
RUN nvm install 8.2.1

RUN pip3 install --upgrade pip
RUN pip3  install -e .
RUN pip3 install pytest

WORKDIR /tests/

CMD pytest -x