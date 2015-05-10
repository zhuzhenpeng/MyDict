# -*- coding: utf8 -*-
from urllib import request, parse
import json
import configparser


class BaiduTranslator:
    """
    单例模式
    """
    _shared_state = {
        '_API_URL': 'http://openapi.baidu.com/public/2.0/bmt/translate',
        '_AUTO': 'auto',
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

    def translate(self, content):
        params = {
            'client_id': self._CLIENT_ID,
            'q': content,
            'from': self._AUTO,
            'to': self._AUTO
        }
        query_string = parse.urlencode(params)
        response = request.urlopen(self._API_URL + '?' + query_string)
        response_str = response.read().decode('utf-8')
        json_str = json.loads(response_str)
        return json_str


if __name__ == '__main__':
    translator = BaiduTranslator()
    result1 = translator.translate('今天天气很好')
    print(result1)
    result2 = translator.translate('I love you')
    print(result2)