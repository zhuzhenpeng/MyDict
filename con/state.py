class ControllerState:
    """
    控制器管理状态的基类
    """

    @staticmethod
    def alpha(controller, ch):
        raise NotImplementedError()

    @staticmethod
    def enter(controller):
        raise NotImplementedError()

    @staticmethod
    def backspace(controller):
        raise NotImplementedError()

    @staticmethod
    def tab(controller):
        raise NotImplementedError()

    @staticmethod
    def c_g(controller):
        raise NotImplementedError()

    @staticmethod
    def c_p(controller):
        raise NotImplementedError()

    @staticmethod
    def c_n(controller):
        raise NotImplementedError()

    @staticmethod
    def recover(controller):
        raise NotImplementedError()


class SearchControllerState(ControllerState):
    """
    查询状态下的各种操作处理
    """

    @staticmethod
    def _update_relevant(controller):
        """
        根据目前输入的单词刷新补全单词
        根据补全单词更新显示
        更新选中单词的下标
        """
        controller._set_relevant(controller._tree.get_relevant(controller._word))
        controller._cn_last = controller._swin.show_relevant(controller._relevant, 0)
        controller._sindex = 0

    @staticmethod
    def alpha(controller, ch):
        """
        输入字母时刷新字符串
        """
        controller._swin.show_input_word(controller._word)
        SearchControllerState._update_relevant(controller)

    @staticmethod
    def enter(controller):
        """
        查询单词，隐藏查询框
        切换到展示状态并展示单词内容
        """
        meanings, examples = controller._dict.get_meaning(controller._word)
        controller._dwin.clear()
        controller._dwin.display_word(controller._word)
        if len(meanings) != 0:
            controller._dwin.display_meanings(meanings)
            controller._dwin.display_examples(examples)
        else:
            # 查询失败
            controller._dwin.display_search_failed(controller._word)
        controller._change_to_state(DisplayControllerState)
        controller._dwin.refresh()
        # 清空单词
        controller._word = str()

    @staticmethod
    def backspace(controller):
        """
        删除最后一个字母，刷新字符串
        """
        if len(controller._word) == 0:
            controller._change_to_state(DisplayControllerState)
        else:
            controller._swin.show_input_word(controller._word)
            SearchControllerState._update_relevant(controller)

    @staticmethod
    def tab(controller):
        """
        通过当前高亮的单词补全输入单词
        """
        if len(controller._relevant) != 0:
            controller._word = controller._relevant[controller._sindex]
            controller._swin.show_input_word(controller._word)
            SearchControllerState._update_relevant(controller)

    @staticmethod
    def c_g(controller):
        """
        隐藏查询窗口，删除已输入的单词
        """
        controller._word = str()
        controller._change_to_state(DisplayControllerState)
        controller._state.recover(controller)

    @staticmethod
    def c_p(controller):
        """
        候选高亮位置向上移动，如果在顶端则移到低端
        """
        if controller._sindex == 0:
            controller._sindex = controller._cn_last;
        elif controller._sindex >= 1:
            controller._sindex -= 1
        
        controller._swin.show_relevant(controller._relevant, controller._sindex)

    @staticmethod
    def c_n(controller):
        """
        候选高亮位置向下移动，如果在底端则移到顶端
        """
        if controller._sindex == controller._cn_last:
            controller._sindex = 0
        elif controller._sindex < controller._cn_last:
            controller._sindex += 1
        
        controller._swin.show_relevant(controller._relevant, controller._sindex)

    @staticmethod
    def recover(controller):
        """
        恢复查询状态原本的内容
        """
        controller._swin.recover()


class DisplayControllerState(ControllerState):
    """
    展示状态下的各种操作处理
    """

    @staticmethod
    def alpha(controller, ch):
        """
        切换到查询状态
        """
        controller._change_to_state(SearchControllerState)
        controller._state.alpha(controller, ch)

    @staticmethod
    def enter(controller):
        pass

    @staticmethod
    def backspace(controller):
        pass

    @staticmethod
    def tab(controller):
        pass

    @staticmethod
    def c_g(controller):
        """
        退出程序
        """
        raise StopIteration()

    @staticmethod
    def c_p(controller):
        pass

    @staticmethod
    def c_n(controller):
        pass

    @staticmethod
    def recover(controller):
        """
        恢复展示状态原来的内容
        """
        controller._fix()
        controller._dwin.recover()
