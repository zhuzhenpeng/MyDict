import sqlite3

# 单词数据库的建立、插入、查询

CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS words(
        word TEXT,
        meanings TEXT,
        examples TEXT
    )
"""
INSERT_A_WORD = 'INSERT INTO words VALUES (?, ?, ?)'
SEARCH_A_WORD = 'SELECT * FROM words WHERE word=?'


class DictDB:
    def __init__(self):
        self.__conn = sqlite3.connect('./dict.db')
        self.__conn.execute(CREATE_TABLE)

    def put_record_into_db(self, record):
        c = self.__conn.cursor()
        word, result = record
        meanings, examples = result.split('|$')
        c.execute(INSERT_A_WORD, (word, meanings, examples))
        self.__conn.commit()
        print('----------' + word + '----------')

    def search_meaning(self, raw_word):
        word = (raw_word.strip(), )
        c = self.__conn.cursor()
        result = c.execute(SEARCH_A_WORD, word).fetchone()
        return result


if __name__ == '__main__':
    print('----测试数据库查词----')
    conn = sqlite3.connect('./dict.db')
    cur = conn.cursor()
    while True:
        word = input('Enter the word: ')
        if word == 'q':
            break
        result = cur.execute(SEARCH_A_WORD, (word, )).fetchone()
        if result is None:
            print(word + ' 没有找到解释')
            continue
        w, meanings, examples = result
        print(w, end='\n\n')
        for meaning in meanings.split('|'):
            print(meaning)
        print()
        for example in examples.split('|'):
            sentence = example.split('#')
            if len(sentence) > 1:
                en = sentence[0]
                zh = sentence[1]
                print(en)
                print(zh)
                print()
