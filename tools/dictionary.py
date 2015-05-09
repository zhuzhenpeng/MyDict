import sqlite3

from elements.words import EnglishWord


class LocalEnToZhDictionary():
    """
    本地词典，通过查询数据库返回结果
    """

    def __init__(self):
        self.SEARCH_A_WORD = \
            'SELECT meanings, examples FROM words WHERE word=?'
        self.__conn = sqlite3.connect('./dict.db')

    def __del__(self):
        self.__conn.close()

    @staticmethod
    def _make_en_word(query_word, query_result):
        """
        :param query_word: 查询的单词
        :param query_result: 数据库查询结果
        :return: 完整的英语单词词条
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
        :param raw_word: 单词，str类型，不保证输入安全
        :return: 英文单词对象
        """
        stripped_word_tuple = (raw_word.strip().lower(), )
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

    def ready(self):
        """
        通过发送一条指令预热数据库
        """
        search_word = ('hello', )
        connection = sqlite3.connect('./dict.db')
        cur = connection.cursor()
        cur.execute(self.SEARCH_A_WORD, search_word).fetchone()
        cur.close()
        connection.close()


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