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
- `./data`に`dictionary.pickle` `gbm.pickle`を置く

```bash
# building the image
docker-compose build

# starting up a container
docker-compose up
```

## 注意書き
- キャッシュをしていないので、同じurlに何度もリクエストが行く可能性がある
- `./data/error.csv`に`oneURL2text.oneURL2text(url)`で出たエラーが書かれる
    - 止めたい場合はコメントアウト！
- ~~doc2Vecの関係で起動が遅い・メモリをかなり消費する~~
    - `MM = util.ModelMaker()`の周辺をコメントアウトで起動は速くなる
        - 当然doc2Vec周りの機能は使えなくなる