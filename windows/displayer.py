import curses
import math
import configparser


class DisplayWordWindow():
    """
    展示以下内容的窗口：
    1 英文单词的中文解释
    2 英文词组的中文解释
    3 中文单词对应的英文解释(英文单词)
    """

    def __init__(self, window):
        """
        :window: curses.newwin()产生的窗口
        """
        self._window = window
        self._maxy, self._maxx = window.getmaxyx()
        self._read_conf()

        # 设置版本号
        self._VERSION = 'MyDict V1.9'
        self._window.addstr(self._maxy - 1, self._maxx - 12,
                            self._VERSION, curses.color_pair(1))

        # 设置欢迎词和自定义文本
        self._window.addstr(self._WELCOME_Y, self._WELCOME_X,
                            self._WELCOME, curses.color_pair(3))

        # 设置欢迎画面
        self._init_pic()

        # 设置单词的坐标
        self._word_display_y = 0

        self._window.refresh()

    def _read_conf(self):
        """
        读取配置文件,可以获得以下的参数：
        1.左上角欢迎词，以及它的坐标
        2.首页图片的坐标
        3.单词解释的坐标
        4.例句的坐标
        """
        config = configparser.ConfigParser()
        config.read('CONFIG')
        self._WELCOME = config['HomePage']['welcome']
        self._WELCOME_X = int(config['HomePage']['welcome_x'])
        self._WELCOME_Y = int(config['HomePage']['welcome_y'])
        if self._WELCOME_X == 0:
            self._WELCOME_X = 2
        if self._WELCOME_Y == 0:
            self._WELCOME_Y = 1

        self._PIC_X = int(config['HomePage']['pic_x'])
        self._PIC_Y = int(config['HomePage']['pic_y'])
        if self._PIC_X == 0:
            self._PIC_X = self._maxx // 8 + 2
        if self._PIC_Y == 0:
            self._PIC_Y = self._WELCOME_Y + 3

        self._MEANINGS_X = int(config['Word']['meanings_x'])
        self._MEANINGS_Y = int(config['Word']['meanings_y'])
        if self._MEANINGS_X == 0:
            self._MEANINGS_X = 1
        if self._MEANINGS_Y == 0:
            self._MEANINGS_Y = 2

        self._EXAMPLES_X = int(config['Word']['examples_x'])
        self._EXAMPLES_Y = 0
        if self._EXAMPLES_X == 0:
            self._EXAMPLES_X = 1

    def _init_pic(self):
        """
        读取起始画面
        当控制台的大小适合时才会读取画面
        """
        lines = []
        max_line_length = 0
        line_cnt = 0

        with open('PICTURE', 'r') as pic_file:
            for line in pic_file:
                if len(line) > max_line_length:
                    max_line_length = len(line)
                line_cnt += 1
                lines.append(line)

        if max_line_length > self._maxx - 6 or line_cnt > self._maxy - 6:
            return
        else:
            pic_y = self._PIC_Y
            for line in lines:
                self._window.addstr(pic_y, self._PIC_X, line)
                pic_y += 1

    def _display_word(self, word):
        """
        展示查询的单词
        """
        word_x = math.floor((self._maxx - len(word)) / 2)
        self._window.addstr(self._word_display_y, word_x, word, curses.color_pair(3))
        self._window.refresh()

    def _display_meanings(self, meanings):
        """
        展示单词解释
        :param meanings:  字符串列表
        """
        y = self._MEANINGS_Y

        increment = 0
        for m in meanings:
            self._window.addstr(y + increment, self._MEANINGS_X, m)
            increment += 2

        # 设置例句的纵坐标
        self._EXAMPLES_Y = y + increment

    def _display_examples(self, examples):
        """
        展示例句
        :param examples:  二元组列表,（英文句子, 中文句子）
        """
        line = '-------------' * 4
        self._window.addstr(self._EXAMPLES_Y, self._EXAMPLES_X,
                            line, curses.color_pair(1))
        increment = 1
        for en, zh in examples:
            en_line_nums = len(en) // (self._maxx - self._EXAMPLES_X) + 1
            zh_line_nums = len(zh) // (self._maxx - self._EXAMPLES_X) + 1
            at_least_lines = self._EXAMPLES_Y + increment + 1 + en_line_nums + zh_line_nums
            if at_least_lines >= self._maxy:
                break
            self._window.addstr(self._EXAMPLES_Y + increment, self._EXAMPLES_X, en)
            increment += en_line_nums
            self._window.addstr(self._EXAMPLES_Y + increment, self._EXAMPLES_X, zh)
            increment += zh_line_nums
            increment += 1

    def _display_search_failed(self, failed_word):
        """
        没有找到单词释义时的输出内容
        """
        sentence = '没有找到' + failed_word + '相关解释'
        sentence_x = (self._maxx - len(sentence) - 8) // 2
        self._window.addstr(self._maxy // 2, sentence_x,
                            sentence, curses.color_pair(1))

    def display_en_word(self, explained_word):
        """
        展示英文单词的查询结果
        """
        self._display_word(explained_word.word)
        if explained_word.is_valid():
            self._display_meanings(explained_word.explanations)
            self._display_examples(explained_word.zh_example_sentence)
        else:
            self._display_search_failed(explained_word.word)

    def recover(self):
        """
        恢复窗口内容
        """
        self._window.touchwin()
        self._window.refresh()

    def refresh(self):
        """
        刷新窗口
        """
        self._window.refresh()


    def clear(self):
        """
        清空屏幕
        """
        self._window.clear()
