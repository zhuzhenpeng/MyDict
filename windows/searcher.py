import curses


class SearchWindow():
    """
    进行单词查询时左侧的窗口
    """

    def __init__(self, input_win, relevant_win):
        """
        :input_win:     输入单词的窗口
        :relevant_win:  显示相关单词的窗口
        """
        self._input_window = input_win
        self._relevant_window = relevant_win
        self._rmaxy, self._rmaxx = relevant_win.getmaxyx()

    def _fix(self):
        """
        修复窗口，让窗口在任何情况下都显示以下内容
        """
        self._input_window.border('|', '|', '-', '-',
                                  '+', '+', '+', '+')
        self._relevant_window.border('|', '|', '-', '-',
                                     '+', '+', '+', '+')
        self.refresh()

    def recover(self):
        """
        恢复窗口
        """
        self._input_window.touchwin()
        self._relevant_window.touchwin()
        self.refresh()

    def refresh(self):
        """
        刷新窗口
        """
        self._input_window.refresh()
        self._relevant_window.refresh()

    def show_input_word(self, word):
        """
        展示输入的单词
        """
        self._input_window.clear()
        self._input_window.addstr(1, 1, word)
        self._fix()

    def show_relevant(self, relevant, highlight_index):
        """
        展示候选单词
        :relevant:          备选词集合，数量有可能大于能显示的数量
        :highlight_index:   需要高亮的备选词下标
        :return:            最后一个能显示的单词的下标
        """
        self._relevant_window.clear()
        word_y = 1
        max_index = 0
        for word in relevant:
            if word_y > self._rmaxy - 2:
                break
            if max_index == highlight_index:
                self._relevant_window.addstr(word_y, 1, word, curses.color_pair(1))
            else:
                self._relevant_window.addstr(word_y, 1, word)
            word_y += 1
            max_index += 1
        self._fix()
        return max_index - 1