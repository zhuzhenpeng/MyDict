from con.base_displayer import DisplayInterface
import curses
import math
import configparser


class DisplayWindow(DisplayInterface):

    def __init__(self, window):
        """
        :window: curses.newwin()产生的窗口
        """
        self._window = window
        self._maxy, self._maxx = window.getmaxyx()
        self._read_conf()

        # 设置版本号
        self._VERSION = 'MyDict V1.0'
        self._window.addstr(self._maxy-1, self._maxx-12, self._VERSION, curses.color_pair(1))

        # 设置欢迎词和自定义文本
        self._window.addstr(self._WELCOME_Y, self._WELCOME_X, self._WELCOME, curses.color_pair(3))

        # 设置单词的坐标
        self._word_x = math.floor(self._maxx * 0.45)
        self._word_y = 0

        self._window.refresh()

    def _read_conf(self):
        """
        读取配置文件
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

    def display_word(self, word):
        """
        展示查询的单词
        """
        self._window.addstr(self._word_y, 1, word, curses.color_pair(3))
        self._window.addstr(self._word_y, self._word_x, word, curses.color_pair(3))
        self._window.addstr(self._word_y, self._maxx-len(word)-1, word, curses.color_pair(3))
        self._window.refresh()

    def display_meanings(self, meanings):
        """
        展示单词解释
        每个解释用|分割
        """
        ms = meanings.split('|')
        y = self._MEANINGS_Y

        increment = 0
        for m in ms:
            self._window.addstr(y+increment, self._MEANINGS_X, m)
            increment += 2

        # 设置例句的纵坐标
        self._EXAMPLES_Y = y + increment

    def display_examples(self, examples):
        """
        展示例句
        每个例句用#分割，例句中的中英文用|分割
        """
        line = '-------------' * 4
        self._window.addstr(self._EXAMPLES_Y, self._EXAMPLES_X, line, curses.color_pair(1))
        increment = 1
        for example in examples.split('|'):
            sentence = example.split('#')
            if len(sentence) > 1:
                en = sentence[0]
                zh = sentence[1]
                en_line_nums = len(en) // (self._maxx-self._EXAMPLES_X) + 1 
                zh_line_nums = len(zh) // (self._maxx-self._EXAMPLES_X) + 1
                at_least_lines = self._EXAMPLES_Y + increment + 1 +\
                        en_line_nums + zh_line_nums
                if at_least_lines >= self._maxy:
                    break
                self._window.addstr(self._EXAMPLES_Y+increment, self._EXAMPLES_X, en)
                increment += en_line_nums
                self._window.addstr(self._EXAMPLES_Y+increment, self._EXAMPLES_X, zh)
                increment += zh_line_nums
                increment += 1

    def display_search_failed(self, failed_word):
        """
        查询失败
        """
        self._window.addstr(self._maxy//2, self._maxx//2-14, 
                '没有找到'+failed_word+'相关解释',
                curses.color_pair(1))


    def recover(self):
        self._window.touchwin()
        self._window.refresh()


    def refresh(self):
        self._window.refresh()

    
    def clear(self):
        self._window.clear()
