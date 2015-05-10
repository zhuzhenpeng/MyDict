# -*- coding: utf8 -*-


class Word:
    def __init__(self, content):
        self.content = content
        self.explanations = []

    def add_explanation(self, explanation):
        self.explanations.append(explanation)

    def is_valid(self):
        """
        如果该词(词组)有解释说明这是一个正确的词
        """
        return len(self.explanations) > 0


class EnglishWord(Word):
    """
    英文单词、词组
    包括单词本身，中文解释，中文例句
    """

    def __init__(self, word):
        super().__init__(word)
        self.zh_example_sentence = []

    def __getattr__(self, item):
        if item == 'word':
            return self.content
        else:
            return None

    def add_example_sentence(self, sentence):
        self.zh_example_sentence.append(sentence)


# class EnglishPhrase(Word):
#     """
#     英文词组
#     包含词组本身，词组解释
#     """
#
#     def __init__(self, phrase):
#         super().__init__(phrase)
#
#     def __getattr__(self, item):
#         if item == 'phrase':
#             return self.content
#         else:
#             return None


class ChineseWord(Word):
    """
    中文单词
    办案中文单词本身，相对应的英文解释
    """

    def __init__(self, word):
        super().__init__(word)

    def __getattr__(self, item):
        if item == 'word':
            return self.content
        else:
            return None