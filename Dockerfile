FROM python:3.8

RUN apt-get update && apt-get install -q -y \
    mecab \ 
    libmecab-dev \ 
    mecab-ipadic-utf8 \ 
    python-mecab \
    file \
    sudo

RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git > /dev/null 
RUN mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -y --ignore_noun_ortho --ignore_noun_sahen_conn_ortho

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]