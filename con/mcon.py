# coding=utf-8
from con.state import WordDisplay
from tools import trie
from tools.dictionary import LocalEnToZhDictionary, OnlineDictionary
import string
from tools.translator import OnlineTranslator


class MainController:
    """
    核心控制器，接收用户输入
    调用model处理输入，刷新view
    """

    def __init__(self, main_win, wm_win, sch_win, tran_win):
        """
        :param main_win:curses初始化时产生的窗口
        :param wm_win:查询结果展示窗口
        :param sch_win:搜索窗口
        """
        self.main_window = main_win
        self.word_meanings_window = wm_win
        self.search_window = sch_win
        self.translation_window = tran_win

        # 初始化状态
        self.state = WordDisplay
        self.change_to_state(WordDisplay)

        # 词典树
        self.trie = trie.get_trie()
        # 当前输入单词
        self.input_word = str()
        # 当前输入单词最大长度限制
        self.word_max_length = sch_win.max_word_width()
        # 当前候选单词集合
        self.relevant_words = None
        # 高亮单词的下标
        self.selected_index = 0
        # 备选单词的显示出来的数量-1，用于c-n的下界判断
        self.cn_last = 0

        # 待翻译的句子
        self.input_sentence = str()

        # 本地词典
        self.local_dict = LocalEnToZhDictionary()
        # 在线词典
        self.online_dict = OnlineDictionary()

        # 在线翻译工具
        self.translator = OnlineTranslator()

        # 中文符号的unicode
        self.zh_punctuations = {
            '，', '。', '？', '！', '；', '、', '“', '‘', '【', '】',
            '（', '）', '《', '》', '￥'
        }

    @staticmethod
    def _is_word_input(char_num):
        """
        判断输入字符是否为英文、中文或空格
        :param char_num: 字符对应的unicode码
        """
        if (65 <= char_num <= 90 or 97 <= char_num <= 122) \
                or (char_num == 32) or (0x4e00 <= char_num <= 0x9fa5):
            return True
        else:
            return False

    def _is_punctuation_input(self, p):
        """
        判断输入是否是标点符号符号
        :param p: 标点符号对应的unicode码
        :return:
        """
        return chr(p) in string.punctuation or chr(p) in self.zh_punctuations

    def work(self):
        """
        进入工作循环，捕捉键盘输入
        """
        while True:
            try:
                character = self.main_window.get_wch()
                ch_num = ord(character)

                # 字符输入
                if self._is_word_input(ch_num):
                    self.state.alpha(self, character)

                # 符号输入
                if self._is_punctuation_input(ch_num):
                    self.state.punctuation(self, character)

                # 输入Esc
                if ch_num == 27:
                    self.state.esc(self)

                # 输入BackSpace,也相当于OS X中的delete
                if ch_num == 127:
                    self.state.backspace(self)

                # 输入C-l
                if ch_num == 12:
                    self.state.c_l(self)

                # 输入Enter
                if ch_num == 10:
                    self.state.enter(self)

                # 输入C-n
                if ch_num == 14:
                    self.state.c_n(self)

                # 输入C-p
                if ch_num == 16:
                    self.state.c_p(self)

                # 输入Tab
                if ch_num == 9:
                    self.state.tab(self)

                # 输入C-k
                if ch_num == 11:
                    self.state.c_k(self)

            except StopIteration:
                break

    def change_to_state(self, state):
        """
        改变当前工作状态：查询/展示
        :state: 由state模块定义的对象
        """
        self.state = state
        self.state.recover(self)

    def fix_background(self):
        """
        刷新self.main_window,修复边框
        """
        self.main_window.touchwin()
        self.main_window.refresh()

    def set_relevant(self, relevant):
        """
        按字母排序并设置相关单词集合
        """
        self.relevant_words = sorted(relevant)
