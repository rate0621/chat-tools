import urllib.request
from urllib.parse import quote
import json
import re
import os
import sys
import random
import requests
import pprint


class Tools():
    def getImageUrl(self, search_item):
        '''
        googleのcustom serachを利用して引数で指定した文字列の画像を取得する
        Line messaging api の仕様上、画像のURLがhttpsでないとAPIが受け付けてくれないため、httpのURLだった場合はスルーして次の画像（URL）を評価する
        一度のリクエストで10件までしか取得できないため、もし10件ともhttpのリンクだった場合はからのリストが返される。
        @param  検索文字列（str）
        @return 画像のリンクURL（list）
        '''
        GOOGLE_SEACH_API_KEY = os.getenv("GOOGLE_SEACH_API_KEY")
        CUSTOM_SEARCH_ENGINE = os.getenv("CUSTOM_SEARCH_ENGINE")

        if not GOOGLE_SEACH_API_KEY:
            print("環境変数[GOOGLE_SEACH_API_KEY]が設定されていません。")
            sys.exit()

        if not CUSTOM_SEARCH_ENGINE:
            print("環境変数[CUSTOM_SEARCH_ENGINE]が設定されていません。")
            sys.exit()

        img_list = []
        query_img = "https://www.googleapis.com/customsearch/v1?key=" + GOOGLE_SEACH_API_KEY + \
            "&cx=" + CUSTOM_SEARCH_ENGINE + "&num=10&start=1&q=" + \
            quote(search_item) + "&searchType=image"
        res = urllib.request.urlopen(query_img)
        data = json.loads(res.read().decode('utf-8'))
        for j in range(len(data["items"])):
            if re.search('https', data["items"][j]["link"]):
                img_list.append(data["items"][j]["link"])
                break

        return img_list

    def textChallenge(self, text):
        s = ''.join(random.sample(text, len(text)))
        return s

    def translateText(self, text, to_lang):
        API_URL = 'https://api-free.deepl.com/v2/translate'
        AUTH_KEY = os.environ["DEEPL_AUTH_KEY"]

        response = requests.get(
            API_URL,
            params={
                'auth_key': AUTH_KEY,
                'text': text,
                'target_lang': to_lang
            }
        )

        d = json.loads(response.text)
        return d


if __name__ == "__main__":
    args = sys.argv
    tools = Tools()
    img_url = tools.getImageUrl(args[1])
    print(img_url)
