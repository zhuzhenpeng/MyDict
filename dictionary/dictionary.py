from con.base_dict import DictionaryInterface
import sqlite3

class Dictionary(DictionaryInterface):
    """
    字典，作为整个程序的model部分
    """

    def __init__(self):
        self.SEARCH_A_WORD = \
                'SELECT meanings, examples FROM words WHERE word=?'

        self.__conn = sqlite3.connect('./dict.db')

    def get_meaning(self, word):
        """
        获取单词释义
        :word:      单词，str类型，不保证输入安全
        :return:    返回单词的解释和例句
        """
        word = (word.strip().lower(), )
        c = self.__conn.cursor()
        result = c.execute(self.SEARCH_A_WORD, word).fetchone()
        if result is None:
            result = ('', '')
        return result
