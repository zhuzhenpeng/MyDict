import requests
from bs4 import BeautifulSoup

website = "http://dict.baidu.com/s"


def get_meaning(soup):
    """
    解析获取单词解释
    不同解释间用|分割

    :soup:  网页的Beautiful对象
    :return:包含全部中文解释的字符串
            若没有找到则返回None
    """

    result = str()
    # 获取单词中文解释并放在结果集中
    zhn_meanings = soup.find(attrs={'id': 'en-simple-means'})
    if zhn_meanings is not None:
        zhn_meanings = zhn_meanings.div
        for p_node in zhn_meanings.find_all(name='p', recursive=False):
            if p_node.strong.string is not None:
                result += str(p_node.strong.string)
                result += ' '
            if p_node.span.string is not None:
                result += str(p_node.span.string)
                result += '|'

        return result
    else:
        zhn_meanings = soup.find(attrs={'id': 'fanyi-content'})
        if zhn_meanings is None:
            return None
        else:
            result = str(zhn_meanings.string)
            return result.strip() + '|'


def get_example(soup):
    """
    解析获取单词例句，一句例句由英文和相应中文解释组成
    不同例句间由|分割，中英文句子用#分割

    :soup:  网页的BeautifulSoup对象
    :return:包含全部例句的字符串
    """

    # 例句在网页上是经过js处理展现的，现在获取的是原始的格式化数据
    # 原始数据放在var example_data = [...]中，格式大致如下：
    """
    [
        [例句1
            [英文
                [How][are][you][?]
            ]
            [中文
                [你][怎么样][？]
            ]
            例句来源网址
        ]
        ...
        [例句n
            ...
        ]
    ] 
    """
    # 规律：需要提取的词在四个左中括号内，即[[[[
    # 如果[]互相抵消，那么只剩两个[[时表示新的一句话，中文或英文

    # 从网页中抓取格式化数据
    text = soup.find(name='div', attrs={'id': 'example-box'})
    try:
        text = str(text.next_sibling.next_sibling.string)
    except AttributeError:
        return ' '
    begin = text.find('example_data') + 15
    end = text.find(']];') + 2
    format_data = text[begin:end]

    # 解析格式化数据，使用上面描述的规律，根据[的数量分析
    left_bracket_nums = 0
    next_word = False
    quote_flag = 0  #双引号标识
    example_index = 0  #例句下标，偶数时为英语句子，单数时为中文句子
    transferred_flag = False  #转义字符标识
    word = str()
    sentence = str()
    for ch in format_data:
        if ch == '[':
            left_bracket_nums += 1
            if left_bracket_nums == 4:
                next_word = True
            continue

        if ch == '"' and transferred_flag:
            sentence += '"'
            transferred_flag = False
            continue

        if ch == "'" and transferred_flag:
            sentence = sentence[:-1]
            sentence += "'"
            transferred_flag = False
            continue

        if ch == '"' and next_word:
            quote_flag += 1
            if quote_flag == 2:
                next_word = False
                quote_flag = 0
                if example_index % 2 == 0:
                    if len(word) == 1 and not word.isalnum():
                        sentence = sentence[:-1]
                    sentence += word
                    sentence += ' '
                else:
                    sentence += word
                word = str()
            continue

        if next_word and ch != '\\':
            word += ch
            continue

        if next_word and ch == '\\':
            transferred_flag = True

        if ch == ']':
            left_bracket_nums -= 1
            if left_bracket_nums == 2:
                sentence += '#'
                example_index += 1
            if left_bracket_nums == 1:
                sentence += '|'
            continue

    return sentence


def get_explain_from_web(word):
    """
    Get word explain from baidu.

    :word:  英文单词
    :return:单词的解释和例句,格式如下:
                解释1|$例句1英文部分#例句2中文部分|
    """
    word = word.strip()
    query_word = {'wd': word}
    page = requests.get(website, params=query_word)

    if page.status_code != requests.codes.ok:
        page.raise_for_status()

    soup = BeautifulSoup(page.text)
    meanings = get_meaning(soup)
    if meanings is None:
        return None
    examples = get_example(soup)

    return meanings + '$' + examples


if __name__ == '__main__':
    print('----测试从网上爬解释----')
    while True:
        word = input('Enter the word: ')
        if word == 'q':
            break
        result = get_explain_from_web(word)
        if result is None:
            print(word + ' 没有找到解释')
            continue
        meanings, examples = result.split('|$')
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
