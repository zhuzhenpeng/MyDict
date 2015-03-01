import curses
from con.state import SearchControllerState
from con.state import DisplayControllerState

class MainController:
    """
    核心控制器，接收用户输入
    调用model处理输入，刷新view
    """

    def __init__(self, main_win, dis_win, sch_win,
            dictionary, t):
        """
        :main_win:  curses初始化时产生的窗口
        :dis_win:   查询结果展示窗口
        :sch_win:   搜索窗口
        :dictionary:词典
        :t:         字典树
        """
        self._main_win = main_win
        self._dwin = dis_win
        self._swin = sch_win
        self._dict = dictionary
        self._word = str()

        # 捕获特殊按键
        self._main_win.keypad(True)
        self._main_win.border('|', '|', '-', '-', '+', '+', '+', '+')
        self._main_win.refresh()

        # 词典树
        self._tree = t
        # 当前候选单词集合
        self._relevant = None
        # 选中单词在候选队列中的下标
        self._sindex = 0
        # 备选单词的显示出来的数量-1，用于c-n的下界判断
        self._cn_last = 0

        # 初始化状态
        self._change_to_state(DisplayControllerState)


    def work(self):
        """
        进入工作循环，捕捉键盘输入
        """
        while True:
            try:
                raw_ch = self._main_win.getch()

                # 输入字母
                if (raw_ch >= 65 and raw_ch <= 90) or \
                        (raw_ch >= 97 and raw_ch <=122):
                        if len(self._word) < 26:
                            self._word += chr(raw_ch)
                        self._state.alpha(self, raw_ch)

                # 输入C-g
                if raw_ch == 7:
                    self._state.c_g(self)

                # 输入BackSpace
                if raw_ch == curses.KEY_BACKSPACE:
                    self._word = self._word[:-1]
                    self._state.backspace(self)

                # 输入Enter
                if raw_ch == ord('\n'):
                    self._state.enter(self)

                # 输入C-n
                if raw_ch == 14:
                    self._state.c_n(self)

                # 输入C-p
                if raw_ch == 16:
                    self._state.c_p(self)

                # 输入Tab
                if raw_ch == ord('\t'):
                    self._state.tab(self)

            except StopIteration:
                break

    def _change_to_state(self, state):
        """
        改变当前工作状态：查询/展示
        :state: 由state模块定义的对象
        """
        self._state = state
        self._state.recover(self)

    def _fix(self):
        """
        刷新self._main_win,修复边框
        """
        self._main_win.touchwin()
        self._main_win.refresh()

    def _set_relevant(self, relevant):
        """
        按字母排序并设置相关单词集合
        """
        self._relevant = sorted(relevant)
