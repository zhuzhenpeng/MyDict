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
        config.read('CONFIG', encoding='utf-8')
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

    def parse_result(result):
        print(result['trans_result'][0]['dst'])

    translator = BaiduTranslator()
    result1 = translator.translate('今天天气很好')
    print(result1)
    parse_result(result1)
    result2 = translator.translate('I love you')
    print(result2)
    parse_result(result2)
    result3 = translator.translate('sdfsdfasdfasf')
    print(result3)
    parse_result(result3)
    result4 = translator.translate('士大夫士大夫就是地方你说的')
    print(result4)
    parse_result(result4)