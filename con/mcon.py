# coding=utf-8
import curses

from con.state import DisplayControllerState
from tools import trie
from tools.dictionary import LocalEnToZhDictionary, OnlineDictionary


class MainController:
    """
    核心控制器，接收用户输入
    调用model处理输入，刷新view
    """

    def __init__(self, main_win, dis_win, sch_win):
        """
        :param main_win:curses初始化时产生的窗口
        :param dis_win:查询结果展示窗口
        :param sch_win:搜索窗口
        """
        self.main_window = main_win
        self.display_window = dis_win
        self.search_window = sch_win

        # 初始化状态
        self.state = DisplayControllerState
        self.change_to_state(DisplayControllerState)

        # 词典树
        self.trie = trie.get_trie()
        # 当前输入单词
        self.current_word = str()
        # 当前输入单词最大长度限制
        self.word_max_length = sch_win.max_word_width()
        # 当前候选单词集合
        self.relevant_words = None
        # 高亮单词的下标
        self.selected_index = 0
        # 备选单词的显示出来的数量-1，用于c-n的下界判断
        self.cn_last = 0

        # 本地词典
        self.local_dict = LocalEnToZhDictionary()
        # 在线词典
        self.online_dict = OnlineDictionary()

    def work(self):
        """
        进入工作循环，捕捉键盘输入
        """
        while True:
            try:
                raw_ch = self.main_window.getch()

                # 输入字母或空格
                if (65 <= raw_ch <= 90) or (97 <= raw_ch <= 122) \
                        or (raw_ch == 32):
                    # 忽略首字符时空格的输入
                    if raw_ch == 32 and len(self.current_word) == 0:
                        continue
                    if len(self.current_word) < self.word_max_length:
                        self.current_word += chr(raw_ch)
                    self.state.alpha(self, raw_ch)

                # 输入C-g
                if raw_ch == 7:
                    self.state.c_g(self)

                # 输入BackSpace
                if raw_ch == curses.KEY_BACKSPACE:
                    self.current_word = self.current_word[:-1]
                    self.state.backspace(self)

                # 输入Enter
                if raw_ch == ord('\n'):
                    self.state.enter(self)

                # 输入C-n
                if raw_ch == 14:
                    self.state.c_n(self)

                # 输入C-p
                if raw_ch == 16:
                    self.state.c_p(self)

                # 输入Tab
                if raw_ch == ord('\t'):
                    self.state.tab(self)

            except StopIteration:
                break

    def change_to_state(self, state):
        """
        改变当前工作状态：查询/展示
        :state: 由state模块定义的对象
        """
        self.state = state
        self.state.recover(self)

    def fix(self):
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