from abc import ABCMeta, abstractmethod


class SearchInterface(metaclass=ABCMeta):
    """
    查询窗口的接口
    """

    @abstractmethod
    def recover(self):
        """
        恢复窗口内容
        """
        pass

    @abstractmethod
    def refresh(self):
        """
        刷新窗口
        """
        pass

    @abstractmethod
    def show_input_word(self, word):
        """
        展示输入的单词
        """
        pass

    @abstractmethod
    def show_relevant(self, relevant, highlight_index):
        """
        展示候选单词
        """
        pass
