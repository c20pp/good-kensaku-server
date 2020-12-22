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
        text = oneURL2text.oneURL2text(url)
        texts.append(text)
    MM = util.ModelMaker()
    df = MM.loadDataFrame(texts)
    with open("/usr/src/app/data/model_ver_1_0_0.pickle", mode="rb") as fp:
        classifier = pickle.load(fp)
    response = classifier.predict(df)

    return response
