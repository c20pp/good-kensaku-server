import connexion
import six

import random

from swagger_server.models.body import Body  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server import util


def filters(body):  # noqa: E501
    """urlから判断する

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse200
    """
    if connexion.request.is_json:
        body = Body.from_dict(connexion.request.get_json())  # noqa: E501
    response = {
        "results": []
    }
    for _, _ in enumerate(body.urls):
        # ランダムな整数を生成
        response["results"].append(random.randint(0, 1))
    return response
