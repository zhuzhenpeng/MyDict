import curses
import math
import os
import locale

from con.mcon import MainController
from windows.displayer import DisplayWordWindow
from windows.searcher import SearchWindow


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

    # 设置主窗口属性
    # screen.keypad(True)
    screen.border('|', '|', '-', '-', '+', '+', '+', '+')
    screen.refresh()

    # 初始化展示窗口
    display_y, display_x = screen.getmaxyx()
    display_win = DisplayWordWindow(curses.newwin(
        display_y - 2, display_x - 2, 1, 1))

    # 初始化查询窗口
    search_y, search_x = screen.getmaxyx()
    search_x = math.floor(search_x * 0.3)
    search_win = SearchWindow(
        curses.newwin(3, search_x, 0, 0),
        curses.newwin(search_y - 3, search_x, 3, 0))

    # 初始化控制器
    controller = MainController(screen, display_win,
                                search_win)

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
