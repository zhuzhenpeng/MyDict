import sqlite3


class LocalEnToZhDictionary():
    """
    本地词典，通过查询数据库返回结果
    """

    def __init__(self):
        self.SEARCH_A_WORD = \
            'SELECT meanings, examples FROM words WHERE word=?'

        self.__conn = sqlite3.connect('./dict.db')

    def __def__(self):
        self.__conn.close()

    def get_meaning(self, word):
        """
        获取单词释义
        :word:      单词，str类型，不保证输入安全
        :return:    返回二元组：
                    (解释1|解释2|...解释n, 例句1|例句2|...例句n)
                    每个例句中，中英文句子用'#'分割
        """
        word = (word.strip().lower(), )
        c = self.__conn.cursor()
        result = c.execute(self.SEARCH_A_WORD, word).fetchone()
        # 由于数据库的存储格式就是返回格式，因此不做处理
        # 程序中的其它模块是高度依赖这个格式的，保持该格式时此处的责任
        if result is None:
            result = ('', '')
        c.close()
        return result

    def ready(self):
        """
        通过发送一条指令预热数据库
        """
        word = ('hello', )
        conn = sqlite3.connect('./dict.db')
        c = conn.cursor()
        c.execute(self.SEARCH_A_WORD, word).fetchone()
        c.close()
        conn.close()
