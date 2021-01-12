import connexion
import six

import random

from swagger_server.models.body import Body  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server import util
from swagger_server import oneURL2text
from swagger_server import html2text
import pickle


def filters(body):  # noqa: E501
    """urlから判断する

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse200
    """
    if connexion.request.is_json:
        body = Body.from_dict(connexion.request.get_json())  # noqa: E501
    response = []
    texts = []
    for _, url in enumerate(body.urls):
        try:
            text = oneURL2text.oneURL2text(url)
            texts.append(text)
        except Exception as e:
            with open("/usr/src/app/data/error.csv", mode="a") as f:
                f.writelines([str(e), ", ", url, "\n"])
            raise e
    
    predictor = util.Predictor()
    df = predictor.predict(texts)
    with open("/usr/src/app/data/model.pickle", mode="rb") as fp:
        classifier = pickle.load(fp)
    response = classifier.predict(df).tolist()

    return response
