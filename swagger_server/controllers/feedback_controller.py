import connexion
import six

from swagger_server.models.body1 import Body1  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server import util
from swagger_server.controllers.default_controller import redis
from swagger_server import __main__


def feedback(body):  # noqa: E501
    """良いか悪いかをユーザーが判断

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Body1.from_dict(connexion.request.get_json())  # noqa: E501

    if rslt := redis.get(body.url):
        with open(f"{__main__.DATA_PATH}/feedback.csv", mode="a") as f:
            f.writelines([body.url, ", ", str(
                body.user_evaluation), ", ", rslt.decode(), "\n"])
    else:
        respose = InlineResponse400.from_dict({})
        respose.message = "urlを解析していない"
        return respose, 400

    return
