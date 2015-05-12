# coding=utf-8
import re


class ControllerState:
    """
    控制器管理状态的基类
    """

    @staticmethod
    def alpha(controller, ch):
        pass

    @staticmethod
    def enter(controller):
        pass

    @staticmethod
    def backspace(controller):
        pass

    @staticmethod
    def c_w(controller):
        pass

    @staticmethod
    def tab(controller):
        pass

    @staticmethod
    def esc(controller):
        pass

    @staticmethod
    def c_p(controller):
        pass

    @staticmethod
    def c_n(controller):
        pass

    @staticmethod
    def recover(controller):
        pass


class SearchControllerState(ControllerState):
    """
    查询状态下的各种操作处理
    """

    en_chars = r'[a-zA-Z]'

    @staticmethod
    def _update_relevant(controller):
        """
        根据目前输入的单词刷新补全单词
        根据补全单词更新显示
        更新选中单词的下标
        """
        controller.set_relevant(controller.trie.get_relevant(controller.current_word))
        controller.cn_last = controller.search_window.show_relevant(controller.relevant_words, 0)
        controller.selected_index = 0

    @staticmethod
    def _search_en_word(controller):
        if controller.relevant_words:
            explained_word = controller.local_dict.get_meaning(controller.current_word)
        else:
            explained_word = controller.online_dict.get_en_word_meaning(controller.current_word)
        return explained_word

    @staticmethod
    def _search_zh_word(controller):
        explained_word = controller.online_dict.get_zh_word_meaning(controller.current_word)
        return explained_word

    @staticmethod
    def alpha(controller, ch):
        """
        输入字母时刷新字符串
        """
        controller.search_window.show_input_word(controller.current_word)
        SearchControllerState._update_relevant(controller)

    @staticmethod
    def enter(controller):
        """
        查询单词，隐藏查询框
        切换到展示状态并展示单词内容
        """
        # 有无relevant_words表示了本地数据库有无结果
        has_en_char = re.search(SearchControllerState.en_chars, controller.current_word)
        controller.display_window.clear()
        if has_en_char:
            explained_word = SearchControllerState._search_en_word(controller)
            controller.display_window.display_en_word(explained_word)
        else:
            explained_word = SearchControllerState._search_zh_word(controller)
            controller.display_window.display_zh_word(explained_word)
        controller.change_to_state(DisplayControllerState)
        controller.display_window.refresh()
        # 清空单词
        controller.current_word = str()

    @staticmethod
    def backspace(controller):
        """
        删除最后一个字母，刷新字符串
        """
        controller.current_word = controller.current_word[:-1]
        if len(controller.current_word) == 0:
            controller.change_to_state(DisplayControllerState)
        else:
            controller.search_window.show_input_word(controller.current_word)
            SearchControllerState._update_relevant(controller)

    @staticmethod
    def c_w(controller):
        """
        删除全部输入
        """
        controller.current_word = str()
        controller.change_to_state(DisplayControllerState)

    @staticmethod
    def tab(controller):
        """
        通过当前高亮的单词补全输入单词
        """
        if len(controller.relevant_words) != 0:
            controller.current_word = controller.relevant_words[controller.selected_index]
            controller.search_window.show_input_word(controller.current_word)
            SearchControllerState._update_relevant(controller)

    @staticmethod
    def esc(controller):
        """
        隐藏查询窗口，删除已输入的单词
        """
        controller.current_word = str()
        controller.change_to_state(DisplayControllerState)
        controller.state.recover(controller)

    @staticmethod
    def c_p(controller):
        """
        候选高亮位置向上移动，如果在顶端则移到低端
        """
        if controller.selected_index == 0:
            controller.selected_index = controller.cn_last
        elif controller.selected_index >= 1:
            controller.selected_index -= 1

        controller.search_window.show_relevant(controller.relevant_words,
                                               controller.selected_index)

    @staticmethod
    def c_n(controller):
        """
        候选高亮位置向下移动，如果在底端则移到顶端
        """
        if controller.selected_index == controller.cn_last:
            controller.selected_index = 0
        elif controller.selected_index < controller.cn_last:
            controller.selected_index += 1

        controller.search_window.show_relevant(controller.relevant_words,
                                               controller.selected_index)

    @staticmethod
    def recover(controller):
        """
        恢复查询状态原本的内容
        """
        controller.search_window.recover()


class DisplayControllerState(ControllerState):
    """
    展示状态下的各种操作处理
    """

    @staticmethod
    def alpha(controller, ch):
        """
        切换到查询状态
        """
        controller.change_to_state(SearchControllerState)
        controller.state.alpha(controller, ch)

    @staticmethod
    def esc(controller):
        """
        退出程序
        """
        raise StopIteration()

    @staticmethod
    def recover(controller):
        """
        恢复展示状态原来的内容
        """
        controller.fix()
        controller.display_window.recover()