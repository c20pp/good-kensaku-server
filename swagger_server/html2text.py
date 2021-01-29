# html to text
from typing import List
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import re
import random

import bs4
assert '4.9.3' <= bs4.__version__, "please upgrade BeautifulSoup"


def getBeautifulSoupBody(html: bytes):
    bodyend_i = html.rfind(b"</body>")
    if bodyend_i == -1:
        bodyend_i = len(html)
    else:
        bodyend_i = bodyend_i + len(b"</body>")
    html = html[max(0, html.find(b"<body>")):bodyend_i]
    body = BeautifulSoup(html.replace(b"</li>", b"\n</li>"), "lxml").find("body")
    del html
    return body

# text_setを生成する
# text_setは各葉ノードのテキストと木構造を表す


def soup2textset(tag, text_set, tag_string):
    for content in tag.contents:
        if isinstance(content, NavigableString):
            #content.string = content.string.replace('\xa9', '(c)').replace('\xa0', '')
            text_set.add(tag_string + content.string)
        elif str.lower(content.name) in ["script", "meta", "style", "header", "footer"]:
            pass
        else:
            # print(content.name)
            soup2textset(content, text_set, tag_string +
                         str.lower(content.name))
    return text_set

# text_setに一致する葉ノードを削除する


def removetags(tag, remove_text_set, tag_string):
    remove_lists = []
    for content in tag.contents:
        if isinstance(content, NavigableString):
            if (tag_string+content.string) in remove_text_set:
                remove_lists.append(content)
        elif str.lower(content.name) in ["script", "meta", "style", "header", "footer"]:
            remove_lists.append(content)
        else:
            removetags(content, remove_text_set,
                       tag_string + str.lower(content.name))
    for content in remove_lists:
        content.extract()
    del remove_lists

#imgとかを良い感じに処理したい
def converttags(tag):
    for content in tag.contents:
        if isinstance(content, NavigableString):
            pass
        elif str.lower(content.name) == "img":
            content.string = " imageafdiyzbode "
        elif str.lower(content.name) == "code":
            content.string = " codeatusdixhbd "
            content.contents = []
        else:
            converttags(content)


# Webページを取得して解析する
# def html2text(htmls: list(str)) -> list(str):
# 同じドメインのhtml(string)群を受け取って、タグを削除したstringのlistを返す


def html2text(htmls: List[bytes]) -> List[str]:
    # 文字列抽出
    # soups = [BeautifulSoup(html.replace("</li>", "\n</li>"), "html.parser")
    #         for html in htmls[:min(3,len(htmls))]]
    # #bodies = [soup.find("body").text for soup in soups]

    # bodies = [soup.find("body") for soup in soups]
    # del soups
    bodies = [getBeautifulSoupBody(html)
              for html in htmls[:min(3, len(htmls))]]

    # img等のテキスト化
    for body in (bodies):
        converttags(body)

    # 重複の削除
    if 2 <= len(bodies):
        # 重複要素の列挙
        set0 = soup2textset(bodies[0], set(), "")
        set1 = soup2textset(bodies[1], set(), "")
        remove_set = frozenset(set0 & set1)
        if 3 <= len(bodies):
            set2 = soup2textset(bodies[2], set(), "")
            remove_set = frozenset(remove_set | (set2 & set0) | (set2 & set1))
            del set2
        # print(remove_set)
        del set0
        del set1
        # 重複要素の削除
        for i in range(len(bodies)):
            removetags(bodies[i], remove_set, "")

    # soup => textの変換
    for i in range(len(bodies)):
        bodies[i] = bodies[i].text

    # 残り
    for i in range(3, len(htmls)):
        html = htmls[i]
        body = getBeautifulSoupBody(html)
        converttags(body)
        if 2 <= len(bodies):
            removetags(body, remove_set, "")
        bodies.append(body.text)
        del body
        del html
    # del remove_set

    # 空行削除
    emptyline_regex = re.compile('\n\\s*\n')
    for i in range(len(bodies)):
        bodies[i] = emptyline_regex.sub('\n', bodies[i])

    return bodies


def test():
    import os
    path = "/content/drive/Shareddrives/システム設計構築演習/data/sejuku/"
    html_names = os.listdir(path)
    html_names = [html for html in html_names if html[-5:] == ".html"]
    htmls = [open(path + html, 'r', encoding="utf-8").read()
             for html in html_names]
    random.shuffle(htmls)
    bodies = html2text(htmls)

    print(html_names[0])
    print(bodies[0][:100])
    print("........")
    print(bodies[0][-100:])
    print("====================")
    print(html_names[1])
    print(bodies[1][:100])
    print("........")
    print(bodies[1][-100:])
    print("====================")
    print(html_names[2])
    print(bodies[2][:100])
    print("........")
    print(bodies[2][-100:])
    print("====================")
    # print(bodies[0].replace('\xa9', '(c)').replace('\xa0', ''))
    del html_names
    del htmls
    del bodies


if __name__ == "__main__":
    test()
    pass
