import curses
import math
import threading
from con.mcon import MainController
from display.displayer import DisplayWindow
from search.searcher import SearchWindow
from search.trie import Trie
from dictionary.dictionary import Dictionary

# 设置工作目录为当前文件所在的目录
import os

os.chdir(os.path.dirname(__file__))


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


def init_trie():
    # 初始化字典树
    tree = Trie()
    with open('./DBGenerate/words', mode='r') as words:
        for line in words:
            tree.insert(line.strip())
    return tree


def main(screen):
    init_curses()

    # 初始化展示窗口
    display_y, display_x = screen.getmaxyx()
    display_win = DisplayWindow(curses.newwin(
        display_y - 2, display_x - 2, 1, 1))

    # 初始化查询窗口
    search_y, search_x = screen.getmaxyx()
    search_x = math.floor(search_x * 0.3)
    search_win = SearchWindow(
        curses.newwin(3, search_x, 0, 0),
        curses.newwin(search_y - 3, search_x, 3, 0))

    # 初始化字典
    d = Dictionary()

    # 初始化字典树
    tree = init_trie()

    # 初始化控制器
    controller = MainController(screen, display_win,
                                search_win, d, tree)

    # 预热数据库
    db_thread = threading.Thread(target=d.ready)
    db_thread.start()

    # 控制器进入事件循环状态
    controller.work()


if __name__ == '__main__':
    screen = curses.initscr()
    try:
        main(screen)
    finally:
        curses.endwin()
