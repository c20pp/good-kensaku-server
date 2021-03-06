# Swagger generated server

## Overview
This server was generated by the [swagger-codegen](https://github.com/swagger-api/swagger-codegen) project. By using the
[OpenAPI-Spec](https://github.com/swagger-api/swagger-core/wiki) from a remote server, you can easily generate a server stub.  This
is an example of building a swagger-enabled Flask server.

This example uses the [Connexion](https://github.com/zalando/connexion) library on top of Flask.

## Requirements
Python 3.8+

## Usage
open your browser to here:

```
http://localhost:8080/api/ui/
```

To launch the integration tests, use tox:
```
sudo pip install tox
tox
```

## Dockerで動かす
- `data`ディレクトリを作成する
- [ここ](https://drive.google.com/file/d/1t31LE6rq-nny8HlGR7Ijy3IaHA2thpCy/view?usp=sharing)から学習済みのモデルをダウンロードして、`./data`に`dictionary.pickle` `gbm.pickle` `lsi.model` `tfidf.model` `lsi.model.projection`を置く

```bash
# building the image
docker-compose build

# starting up a container
docker-compose up
```

## 注意書き
- ~~キャッシュをしていないので、同じurlに何度もリクエストが行く可能性がある~~
- `./data/error.csv`に`oneURL2text.oneURL2text(url)`で出たエラーが書かれる
    - 止めたい場合はコメントアウト！
