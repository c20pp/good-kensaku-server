import MeCab
from gensim.models.doc2vec import Doc2Vec
from gensim.models import KeyedVectors
import os
import numpy as np


class Embedder:
    def __init__(self, model_type="doc2vec"):
        """
        constructor

        Args:
            model_type (str, optional): Defaults to "doc2vec".
        """
        self.model_type = model_type
        if model_type == "doc2vec":
            self.model = Doc2Vec.load(
                "/usr/src/app/data/jawiki.doc2vec.dbow300d.model")
        elif model_type == "fasttext":
            self.model = KeyedVectors.load_word2vec_format(
                "/usr/src/app/data/fasttext_model.bin", binary=True)

    def _tokenize(self, text):
        """
        分かち書きを行うメソッド

        Args:
            text (str): 入力文字列

        Returns:
            list[str]: 分かち書き済み単語リスト
        """
        wakati = MeCab.Tagger("-Owakati")
        wakati.parse("")
        return wakati.parse(text).strip().split()

    def doc2vec(self, text):
        """
        doc2vec

        Args:
            text (str): string

        Returns:
            numpy.array: embedded vector
        """
        if self.model_type == "doc2vec":
            return self.model.infer_vector(self._tokenize(text))
        elif self.model_type == "fasttext":
            vec_list = []
            for word in self._tokenize(text):
                vec_list.append(self._word2vec(word))
            return np.mean(np.array(vec_list), axis=0)

    def _word2vec(self, word):
        """
        doc2vec

        Args:
            word (str): string

        Returns:
            numpy.array: embedded vector
        """
        # return self.model.get_vector(word)  # same
        return self.model[word]


def main():
    text = 'はじめに今まで自分が使ってきた中で、これは生産性が爆上げする！と思うものを厳選しました是非最後までご覧ください'
    embedder = Embedder()
    print(embedder.doc2vec(text))


if __name__ == "__main__":
    # データ一覧
    """
    html_names = os.listdir("./data/sejuku")
    htmls = [open("./data/sejuku/" + html, 'r', encoding="utf-8").read() for html in html_names]
    bodies = html2text(htmls)
    embedder = Embedder()
    for body in bodies:
        print(embedder.doc2vec(body))
    """
