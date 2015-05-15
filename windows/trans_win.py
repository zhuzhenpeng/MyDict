# coding=utf-8
class TranslatorWindow:
    """
    展示以下内容的窗口：
    1 需要翻译的句子
    2 翻译结果
    """

    def __init__(self, input_win, output_win):
        """
        :param input_win: 显示输入句子的窗口，由curses产生
        :param output_win: 显示输出句子的窗口，由curses产生
        """
        self.input_win = input_win
        self.output_win = output_win
        self._init_output_win()

    def _init_output_win(self):
        self.output_win.clear()
        self.output_win.border(' ', ' ', '-', ' ',
                               ' ', ' ', ' ', ' ')

    def show_input(self, sentence):
        """
        展示需要翻译的句子
        :param sentence: 需要翻译的句子，字符串类型
        """
        self.input_win.clear()
        self.input_win.addstr(0, 1, sentence)
        self.input_win.refresh()

    def show_result(self, result):
        """
        展示翻译结果
        :param result: 翻译结果，字符串类型
        """
        self._init_output_win()
        self.output_win.addstr(1, 1, result)
        self.output_win.refresh()

    def recover(self):
        """
        恢复并显示窗口
        """
        self.input_win.touchwin()
        self.output_win.touchwin()
        self.input_win.refresh()
        self.output_win.refresh()

    def clear_input(self):
        """
        清除输入框的内容
        """
        self.input_win.clear()
        self.input_win.refresh()