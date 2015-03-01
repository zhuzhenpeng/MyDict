from con.base_searcher import SearchInterface
import curses

class SearchWindow(SearchInterface):
    
    def __init__(self, input_win, relevant_win):
        """
        :window: curses.newwin()产生的窗口
        """
        self._iwin = input_win
        self._rwin = relevant_win
        self._rmaxy, self._rmaxx = relevant_win.getmaxyx()

    def _fix(self):
        """
        修复窗口，让窗口在任何情况下都显示以下内容
        """
        self._iwin.border('|', '|', '-', '-', 
                '+', '+', '+', '+')
        self._rwin.border('|', '|', '-', '-', 
                '+', '+', '+', '+')
        self.refresh()


    def recover(self):
        """
        恢复窗口
        """
        self._iwin.touchwin()
        self._rwin.touchwin()
        self.refresh()

    def refresh(self):
        """
        刷新窗口
        """
        self._iwin.refresh()
        self._rwin.refresh()

    def show_input_word(self, word):
        """
        展示输入的单词
        """
        self._iwin.clear()
        self._iwin.addstr(1, 1, word)
        self._fix()

    def show_relevant(self, relevant, highlight_index):
        """
        展示候选单词
        :relevant: 备选词集合
        :highlight_index: 需要高亮的备选词下标
        """
        self._rwin.clear()
        word_y = 1
        max_index = 0
        relevant = sorted(relevant)
        for word in relevant:
            if word_y > self._rmaxy - 2:
                break
            if max_index == highlight_index:
                self._rwin.addstr(word_y, 1, word, curses.color_pair(1))
            else:
                self._rwin.addstr(word_y, 1, word)
            word_y += 1
            max_index += 1
        self._fix()
        return max_index - 1
