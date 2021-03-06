#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from flask_cors import CORS

DATA_PATH = '/usr/src/app/data'


def main():
    options = {"swagger_ui": True}
    app = connexion.App(
        __name__, specification_dir='./swagger/', options=options)
    CORS(app.app)  # allow *
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={
                'title': 'good_kensaku'}, pythonic_params=True)
    app.run(port=8080, debug=True)


if __name__ == '__main__':
    main()
