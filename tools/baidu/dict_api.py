# -*- coding: utf8 -*-
from urllib import request, parse
import json
import configparser


class BaiduDict:
    """
    单例模式
    """
    _shared_state = {
        '_API_URL': 'http://openapi.baidu.com/public/2.0/translate/dict/simple',
        '_ZH': 'zh',
        '_EN': 'en',
        '_CLIENT_ID': None
    }

    def __init__(self):
        self.__dict__ = self._shared_state
        if self._CLIENT_ID is None:
            self._get_api_key()

    def _get_api_key(self):
        config = configparser.ConfigParser()
        config.read('CONFIG')
        self._CLIENT_ID = config['BaiduAPI']['api_key']

    def _query(self, query_content, from_lan, to_lan):
        params = {
            'client_id': self._CLIENT_ID,
            'q': query_content,
            'from': from_lan,
            'to': to_lan
        }
        query_string = parse.urlencode(params)
        response = request.urlopen(self._API_URL + '?' + query_string)
        response_str = response.read().decode('utf-8')
        json_str = json.loads(response_str)
        return json_str

    def en_to_zh(self, en_word):
        """
        英文单词、词组 ——>　中文意思
        :return:百度API返回的json数据
        """
        query_result = self._query(en_word, self._EN, self._ZH)
        return query_result

    def zh_to_en(self, zh_word):
        """
        中文词汇　——> 英文翻译
        :return:百度API返回的json数据
        """
        query_result = self._query(zh_word, self._ZH, self._EN)
        return query_result


if __name__ == '__main__':

    def parse_en(query_result):
        if query_result['data']:
            for items in query_result['data']['symbols'][0]['parts']:
                parts = items['part']
                means = items['means']
                explanation = parts + ' '.join(means)
                print(explanation)
        else:
            print('no explanation')
        print()

    def parse_zh(query_result):
        if query_result['data']:
            for items in query_result['data']['symbols'][0]['parts']:
                means = items['means']
                for explanation in means:
                    print(explanation)
        else:
            print('no explanation')
        print()

    a = BaiduDict()
    q = a.en_to_zh('go on')
    parse_en(q)
    q1 = a.en_to_zh('hello')
    parse_en(q1)
    q3 = a.en_to_zh('asdf')
    parse_en(q3)

    q2 = a.zh_to_en('妈妈')
    parse_zh(q2)
    q5 = a.zh_to_en('阿斯地方各个')
    parse_zh(q5)