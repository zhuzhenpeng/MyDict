import curses
import math
import os
import locale

from con.mcon import MainController
from windows.dict_win import WordMeaningsWindow, SearchWindow
from windows.trans_win import TranslatorWindow


def init_curses():
    # 设置颜色
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_YELLOW, -1)
    curses.init_pair(2, curses.COLOR_WHITE, -1)
    curses.init_pair(3, curses.COLOR_RED, -1)
    curses.init_pair(4, curses.COLOR_BLUE, -1)

    # 不输出键盘的输入
    curses.noecho()

    # 没有输入光标
    curses.curs_set(False)


def main(screen):
    # 设置工作目录为当前文件所在的目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 设置主窗口的边框，主窗口的唯一作用是当背景
    screen.border('|', '|', '-', '-', '+', '+', '+', '+')
    screen.refresh()

    # 初始化单词展示窗口
    wm_y, wm_x = screen.getmaxyx()
    word_meanings_win = WordMeaningsWindow(curses.newwin(
        wm_y - 2, wm_x - 2, 1, 1)
    )

    # 初始化单词查询窗口
    search_y, search_x = screen.getmaxyx()
    search_x = math.floor(search_x * 0.3)
    search_win = SearchWindow(
        curses.newwin(3, search_x, 0, 0),
        curses.newwin(search_y - 3, search_x, 3, 0)
    )

    # 初始化翻译窗口
    tran_y, tran_x = screen.getmaxyx()
    tran_y = (tran_y - 2) // 2
    tran_x -= 2
    tran_win = TranslatorWindow(
        curses.newwin(tran_y, tran_x, 1, 1),
        curses.newwin(tran_y, tran_x, 1 + tran_y, 1)
    )

    # 初始化控制器
    controller = MainController(screen, word_meanings_win,
                                search_win, tran_win)

    # 控制器进入事件循环状态
    controller.work()


if __name__ == '__main__':
    main_screen = curses.initscr()
    locale.setlocale(locale.LC_ALL, '')
    code = locale.getpreferredencoding('utf-8')
    try:
        init_curses()
        main(main_screen)
    finally:
        curses.endwin()
