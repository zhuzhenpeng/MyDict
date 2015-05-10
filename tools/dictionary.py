import sqlite3
import threading

from elements.words import EnglishWord, ChineseWord
from tools.baidu.dict_api import BaiduDict


class LocalEnToZhDictionary():
    """
    本地词典，通过查询数据库返回结果
    """

    def __init__(self):
        self.SEARCH_A_WORD = \
            'SELECT meanings, examples FROM words WHERE word=?'
        self.__conn = sqlite3.connect('./dict.db')
        db_thread = threading.Thread(target=self._ready)
        db_thread.start()

    def __del__(self):
        self.__conn.close()

    @staticmethod
    def _make_en_word(query_word, query_result):
        """
        :param query_word: 查询的单词
        :param query_result: 数据库查询结果
        :return:elements.words.EnglishWord
        """
        explained_word = EnglishWord(query_word)
        meanings, examples = query_result
        # 判断有无结果时,先去掉结果的两边空格，保证无结果和空字符是一致的
        meanings = meanings.strip()
        examples = examples.strip()
        if meanings:
            for meaning in meanings.split('|'):
                explained_word.add_explanation(meaning)
        if examples:
            for example in examples.split('|'):
                if example:
                    sentences = example.split('#')
                    en = sentences[0]
                    zh = sentences[1]
                    explained_word.add_example_sentence((en, zh))
        return explained_word

    def get_meaning(self, raw_word):
        """
        获取单词释义
        :param raw_word: 英文单词,要求str类型
        :return:elements.words.EnglishWord
        """
        stripped_word_tuple = (raw_word.strip(), )
        cursor = self.__conn.cursor()
        query_result = cursor.execute(self.SEARCH_A_WORD, stripped_word_tuple).fetchone()
        # 数据库返回二元组,格式为
        # (解释1|解释2|...解释n, 例句1|例句2|...例句n)
        # 每个例句中，中英文句子用'#'分割,如 My name is Sparrow.#我的名字是Sparrow.#
        if query_result is None:
            query_result = ('', '')
        cursor.close()
        explained_word = self._make_en_word(stripped_word_tuple[0], query_result)
        return explained_word

    def _ready(self):
        """
        通过发送一条指令预热数据库
        """
        search_word = ('hello', )
        connection = sqlite3.connect('./dict.db')
        cur = connection.cursor()
        cur.execute(self.SEARCH_A_WORD, search_word).fetchone()
        cur.close()
        connection.close()


class OnlineDictionary():
    """
    在线词典，通过网络API实时返回解释
    """

    def __init__(self):
        self.dictionary = BaiduDict()

    def get_en_word_meaning(self, en_word):
        """
        在线获取英文单词解释
        :return:elements.words.EnglishWord
        """
        online_query_result = self.dictionary.en_to_zh(en_word)
        return self._parse_baidu_en_result(en_word, online_query_result)

    def get_zh_word_meaning(self, zh_word):
        online_query_result = self.dictionary.zh_to_en(zh_word)
        return self._parse_baidu_zh_result(zh_word, online_query_result)

    @staticmethod
    def _parse_baidu_en_result(en_word, baidu_query_result):
        """
        解析百度返回的json数据
        :return:elements.words.EnglishWord
        """
        explained_word = EnglishWord(en_word)
        if baidu_query_result['data']:
            for items in baidu_query_result['data']['symbols'][0]['parts']:
                parts = items['part']
                means = items['means']
                explanation = parts + ' '.join(means)
                explained_word.add_explanation(explanation)
        return explained_word

    @staticmethod
    def _parse_baidu_zh_result(zh_word, baidu_quety_result):
        """
        解析百度返回的json数据
        :return:elements.words.ChineseWord
        """
        explained_word = ChineseWord(zh_word)
        if baidu_quety_result['data']:
            for items in baidu_quety_result['data']['symbols'][0]['parts']:
                means = items['means']
                for explanation in means:
                    explained_word.add_explanation(explanation)
        return explained_word


if __name__ == '__main__':
    print('查看数据库存储格式')
    word = input('输入单词：')
    SQL_SENTENCE = 'SELECT word, meanings, examples FROM words WHERE word=?'
    conn = sqlite3.connect('./dict.db')
    c = conn.cursor()
    result = c.execute(SQL_SENTENCE, (word,)).fetchone()
    if result is not None:
        word, meanings, examples = result
        print(word)
        print(meanings)
        print(examples)
        print()