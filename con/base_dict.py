from abc import ABCMeta, abstractmethod


class DictionaryInterface(metaclass=ABCMeta):
    """
    字典接口
    """

    @abstractmethod
    def get_meaning(self, word):
        """
        获取单词释义
        :word:      单词，str类型，不保证输入安全
        :return:    返回单词的解释
                    返回格式：
                    解释1|解释2|解释n$例句1|例句2|例句n
        """
        pass
