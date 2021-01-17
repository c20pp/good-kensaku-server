import datetime

import six
import typing

import pandas as pd
from swagger_server import embedder
from swagger_server import __main__
from typing import List

# 以下BoW + lightGBM で必要なimport
import MeCab
import typing
import pandas as pd
import lightgbm as lgb
from typing import List
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from gensim import corpora, models
import re
import pickle


def _deserialize(data, klass):
    """Deserializes dict, list, str into an object.

    :param data: dict, list or str.
    :param klass: class literal, or string of class name.

    :return: object.
    """
    if data is None:
        return None

    if klass in six.integer_types or klass in (float, str, bool):
        return _deserialize_primitive(data, klass)
    elif klass == object:
        return _deserialize_object(data)
    elif klass == datetime.date:
        return deserialize_date(data)
    elif klass == datetime.datetime:
        return deserialize_datetime(data)
    elif hasattr(klass, '__origin__'):
        if klass.__origin__ == list:
            return _deserialize_list(data, klass.__args__[0])
        if klass.__origin__ == dict:
            return _deserialize_dict(data, klass.__args__[1])

    else:
        return deserialize_model(data, klass)


def _deserialize_primitive(data, klass):
    """Deserializes to primitive type.

    :param data: data to deserialize.
    :param klass: class literal.

    :return: int, long, float, str, bool.
    :rtype: int | long | float | str | bool
    """
    try:
        value = klass(data)
    except UnicodeEncodeError:
        value = six.u(data)
    except TypeError:
        value = data
    return value


def _deserialize_object(value):
    """Return a original value.

    :return: object.
    """
    return value


def deserialize_date(string):
    """Deserializes string to date.

    :param string: str.
    :type string: str
    :return: date.
    :rtype: date
    """
    try:
        from dateutil.parser import parse
        return parse(string).date()
    except ImportError:
        return string


def deserialize_datetime(string):
    """Deserializes string to datetime.

    The string should be in iso8601 datetime format.

    :param string: str.
    :type string: str
    :return: datetime.
    :rtype: datetime
    """
    try:
        from dateutil.parser import parse
        return parse(string)
    except ImportError:
        return string


def deserialize_model(data, klass):
    """Deserializes list or dict to model.

    :param data: dict, list.
    :type data: dict | list
    :param klass: class literal.
    :return: model object.
    """
    instance = klass()

    if not instance.swagger_types:
        return data

    for attr, attr_type in six.iteritems(instance.swagger_types):
        if data is not None \
                and instance.attribute_map[attr] in data \
                and isinstance(data, (list, dict)):
            value = data[instance.attribute_map[attr]]
            setattr(instance, attr, _deserialize(value, attr_type))

    return instance


def _deserialize_list(data, boxed_type):
    """Deserializes a list and its elements.

    :param data: list to deserialize.
    :type data: list
    :param boxed_type: class literal.

    :return: deserialized list.
    :rtype: list
    """
    return [_deserialize(sub_data, boxed_type)
            for sub_data in data]


def _deserialize_dict(data, boxed_type):
    """Deserializes a dict and its elements.

    :param data: dict to deserialize.
    :type data: dict
    :param boxed_type: class literal.

    :return: deserialized dict.
    :rtype: dict
    """
    return {k: _deserialize(v, boxed_type)
            for k, v in six.iteritems(data)}


class Predictor:
    def __init__(self) -> None:
        self.mt = MeCab.Tagger("")
    
    def predict(self, texts: List[str]) -> List[int]:
        with open(f'{__main__.DATA_PATH}/dictionary.pickle', mode='rb') as f:
            dictionary = pickle.load(f)
        with open(f'{__main__.DATA_PATH}/gbm.pickle', mode='rb') as f:
            gbm = pickle.load(f)
        tokens = [self._tokenize(text) for text in texts]
        bag = [dictionary.doc2bow(token) for token in tokens]
        tfidf_model = models.TfidfModel(bag)
        tfidf_corpus = tfidf_model[bag]
        lsi_model = models.LsiModel(tfidf_corpus, id2word=dictionary, num_topics=300)
        lsi_corpus = lsi_model[tfidf_corpus]
        vec = [[tup[1] for tup in vec] for vec in lsi_corpus]
        prob = gbm.predict(vec)
        return prob.tolist()

    # 単語に分割する
    def _tokenize(self, text: str) -> List[str]:
        text = re.sub(r'[0-9０-９]+', " ", text)
        return  MeCab.Tagger("-Owakati").parse(text).strip().split()