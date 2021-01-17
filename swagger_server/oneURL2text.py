import os
import requests
from typing import List
import re

from swagger_server import html2text


def get_filename_reg(path: str) -> str:
    res = ""
    for i in range(len(path)-1, -1, -1):
        if path[i] == '/':
            return "[^.\"]*"  # /:id 等
        res += path[i]
        if path[i] == '.':
            break
    return "[^\"]*" + re.escape(res[::-1])


def find_url_from_html(html: str, baseurl: str) -> str:
    domain_match = re.match("https?://[^/\"]+", baseurl)
    if not domain_match:
        print("invalid url: domain not found")
        return None
    domain = domain_match.group(0)
    # print(domain)
    filename_reg = get_filename_reg(baseurl)
    # print(filename_reg)
    url_regex = re.compile(
        "\"(" + re.escape(domain) + ")?/(([^/\"]+/)*" + filename_reg + ")\"")

    found_uri = ""
    longest_prefix = -1
    lengthdiff_min = 0
    # 前方一致が最大で、文字数差が最小なuriを探す
    for match in url_regex.finditer(html):
        matchuri = match.group(2)
        # print(matchuri)
        length = 0
        for i in range(min(len(matchuri), len(baseurl) - len(domain) - 1)):
            if matchuri[i] != baseurl[len(domain)+1+i]:
                break
            length = i+1

        # 完全一致は除外
        if length == len(baseurl) - len(domain) - 1:
            continue

        lengthdiff = abs(len(matchuri) - (len(baseurl) - len(domain) - 1))
        if longest_prefix < length:
            found_uri = matchuri
            longest_prefix = length
            lengthdiff_min = lengthdiff
        elif longest_prefix == length and lengthdiff < lengthdiff_min:
            found_uri = matchuri
            longest_prefix = length
            lengthdiff_min = lengthdiff

    if found_uri == "":
        return ""
    #print(domain + "/" + found_uri)
    return domain + "/" + found_uri


charset_regex = re.compile(
    b"charset\\s*=\\s*['\"]([a-zA-Z0-9_\\-]+)['\"]", flags=re.IGNORECASE)


def decode_to_str(html_content: bytes):
    #html_content = open("test.html", 'rb').read()
    charset = b'utf-8'
    charset_in_html = charset_regex.search(html_content)
    if charset_in_html:
        charset = charset_in_html.group(1)
    return html_content.decode(charset.decode('utf-8'))  # getしたhtml(string)


def oneURL_to_2htmls(url: str) -> List[str]:
    result_htmls = []

    html = requests.get(url)  # getしたhtml(bytes)
    html_code = decode_to_str(html.content)  # getしたhtml(string)
    result_htmls.append(html_code)

    foundurl = find_url_from_html(html_code, url)
    # print(foundurl)
    if foundurl != "":
        html = requests.get(foundurl)  # getしたhtml(bytes)
        html_code = decode_to_str(html.content)  # getしたhtml(string)
        result_htmls.append(html_code)

    return result_htmls


def oneURL2text(url: str) -> str:
    return html2text.html2text(oneURL_to_2htmls(url))[0]


def test():
    oneURL_to_2htmls("https://trap.jp/post/945/")


def test2():
    pass
    base_url = "https://trap.jp/post/945/"
    bodies = html2text.html2text(oneURL_to_2htmls(base_url))
    print(base_url)
    print(bodies[0][:100])
    print("........")
    print(bodies[0][-100:])
    print("====================")
    print("found url")
    print(bodies[1][:100])
    print("........")
    print(bodies[1][-100:])


if __name__ == "__main__":
    # test()
    test2()
    pass
