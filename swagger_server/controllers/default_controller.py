from typing import List
import connexion
import six

from typing import List, Tuple

from swagger_server.models.body import Body  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server import util
from swagger_server import oneURL2text
from swagger_server import html2text
from swagger_server import __main__
import redis


redis = redis.Redis(host='redis', port=6379, db=0)


def filters(body):  # noqa: E501
    """urlから判断する

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse200
    """
    if connexion.request.is_json:
        body = Body.from_dict(connexion.request.get_json())  # noqa: E501
    texts: List[str] = []
    cached_rslt: List[Tuple[int, float]] = []

    calc_urls: List[str] = []

    for i, url in enumerate(body.urls):
        if rslt := redis.get(url):  # type: ignore
            cached_rslt.append((i, float(rslt.decode())))
            continue

        calc_urls.append(url)
        try:
            text = oneURL2text.oneURL2text(url)
            texts.append(text)
        except Exception as e:
            with open(f"{__main__.DATA_PATH}/error.csv", mode="a") as f:
                f.writelines([str(e), ", ", url, "\n"])
            raise e

    results: List[float] = []
    if len(texts) != 0:
        predictor = util.Predictor()
        results = predictor.predict(texts)

        for i, r in enumerate(results):
            redis.set(calc_urls[i], r)  # type: ignore

    for i, r in cached_rslt:
        results.insert(i, r)

    response = InlineResponse200.from_dict({"results": results})

    return response
