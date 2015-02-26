from abc import ABCMeta, abstractmethod


class DisplayInterface(metaclass=ABCMeta):
    """
    展示窗口的接口
    """

    @abstractmethod
    def display_word(self, word):
        """
        展示查询的单词
        """
        pass

    @abstractmethod
    def display_meanings(self, meanings):
        """
        展示单词解释
        每个解释用|分割
        """
        pass

    @abstractmethod
    def display_examples(self, examples):
        """
        展示例句
        每个例句用#分割，例句中的中英文用|分割
        """
        pass


    @abstractmethod
    def display_search_failed(self, failed_word):
        """
        输出搜索失败时的内容
        """
        pass

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
    def clear(self):
        """
        清空屏幕
        """
        pass
