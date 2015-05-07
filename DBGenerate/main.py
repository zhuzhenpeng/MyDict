# -*- coding: utf8 -*-
import persistence
import webdict
import time
from requests.exceptions import RequestException
from multiprocessing import Pool, Process, Queue

# q为全部查询结果队列，多进程共享
q = Queue()

# 将结果集中的结果写入数据库(写进程任务)
def write_result_into_db():
    while True:
        if q.empty():
            time.sleep(1)
        else:
            db_writer.put_record_into_db(q.get(True))


# 从网上抓取单词解释(抓取进程任务)
def get_result_from_web(word):
    try:
        result = webdict.get_explain_from_web(word)
    except RequestException:
        print(word + ' 网络错误，重新查询')
        get_result_from_web(word)

    if result is None:
        print(word + ' 没有找到解释')
    else:
        q.put((word.strip(), result))

if __name__ == '__main__':
    # 初始化数据库
    db_writer = persistence.DictDB()

    # 读取全部单词
    words = []
    with open('words', mode='r') as words_file:
        for word in words_file:
            words.append(word.strip())

    pw = Process(target=write_result_into_db)
    pw.start()
    with Pool(3) as p:
        p.map(get_result_from_web, words)

    pw.join()
