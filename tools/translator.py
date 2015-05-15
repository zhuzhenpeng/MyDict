# coding=utf-8
from tools.baidu.translate_api import BaiduTranslator


class OnlineTranslator:
    """
    在线翻译工具
    """

    def __init__(self):
        self.translator = BaiduTranslator()

    def _parse_baidu_translate_result(self, result):
        return result['trans_result'][0]['dst']

    def translate(self, sentence):
        """
        中英文互相翻译，如果输入为空返回None
        """
        if not sentence:
            return None
        baidu_result = self.translator.translate(sentence)
        return self._parse_baidu_translate_result(baidu_result)