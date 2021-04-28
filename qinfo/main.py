#! /usr/bin/python

import os
import sys
import signal
import curses

import sysinfo


colors = {
    'black': curses.COLOR_BLACK,        # 0
    'red': curses.COLOR_RED,            # 1
    'green': curses.COLOR_GREEN,        # 2
    'yellow': curses.COLOR_YELLOW,      # 3
    'blue': curses.COLOR_BLUE,          # 4
    'magenta': curses.COLOR_MAGENTA,    # 5
    'cyan': curses.COLOR_CYAN,          # 6
    'white': curses.COLOR_WHITE,        # 7
    'default': -1
}

# create cache dir
cache_dir = os.path.expanduser('~') + '/.cache/qinfo'
if not os.path.isdir(cache_dir):
    try: 
        os.makedirs(cache_dir)
    except OSError:
        raise OSError(2, cache_dir + ' not exists')

# traceback Ctrl+C
signal.signal(signal.SIGINT, lambda x,y: sys.exit(0))

def add_unit(stdscr, c_y, c_x, u_data, u_title, u_type):
    st_bar_len = 16 # status bar length
    t_len = 8 # title length

    if u_type == 'cpu':
        # title
        stdscr.addstr(c_y, c_x, u_title, curses.color_pair(2))
        # status bar
        c_x = c_x + t_len
        stdscr.addstr(c_y, c_x, '[', curses.color_pair(2))
        c_x = c_x + 1
        perc = int(u_data['used'])
        st_bar_used = (st_bar_len * perc) / 100
        st_bar_free = st_bar_len - st_bar_used
        if st_bar_used > 0:
            stdscr.addstr(c_y, c_x, '+' * st_bar_used, curses.color_pair(3))
        c_x = c_x + st_bar_len
        stdscr.addstr(c_y, c_x, ']', curses.color_pair(2))
        # used %
        c_x = c_x + 2
        stdscr.addstr(c_y, c_x, str(perc) + '%', curses.color_pair(3))

    if u_type in ('ram'):
        # title
        stdscr.addstr(c_y, c_x, u_title, curses.color_pair(2))
        # status bar
        c_x = c_x + t_len
        stdscr.addstr(c_y, c_x, '[', curses.color_pair(2))
        c_x = c_x + 1
        perc = int((float(u_data['used']) / float(u_data['size'])) * 100)
        st_bar_used = (st_bar_len * perc) / 100
        st_bar_free = st_bar_len - st_bar_used
        if st_bar_used > 0:
            stdscr.addstr(c_y, c_x, '+' * st_bar_used, curses.color_pair(3))
        c_x = c_x + st_bar_len
        stdscr.addstr(c_y, c_x, ']', curses.color_pair(2))
        # used %
        c_x = c_x + 2
        stdscr.addstr(c_y, c_x, str(perc) + '%', curses.color_pair(3))
        # used
        c_x = c_x + 5
        stdscr.addstr(c_y, c_x, u_data['used'] + u_data['used_f'], curses.color_pair(4))
        # size
        c_x = c_x + len(u_data['used'] + u_data['used_f'])
        stdscr.addstr(c_y, c_x, '/' + u_data['size'] + u_data['size_f'], curses.color_pair(4))

    if u_type in ('hdd'):
        # title
        stdscr.addstr(c_y, c_x, u_title, curses.color_pair(2))
        # used %
        c_x = c_x + t_len + 3 + st_bar_len
        perc = int((float(u_data['used']) / float(u_data['size'])) * 100)
        stdscr.addstr(c_y, c_x, str(perc) + '%', curses.color_pair(3))
        # used
        c_x = c_x + 5
        stdscr.addstr(c_y, c_x, u_data['used'] + u_data['used_f'], curses.color_pair(4))
        # size
        c_x = c_x + len(u_data['used'] + u_data['used_f'])
        stdscr.addstr(c_y, c_x, '/' + u_data['size'] + u_data['size_f'], curses.color_pair(4))

def run(stdscr):
    k = 0

    stdscr.clear()
    stdscr.refresh()

    curses.curs_set(0)
    curses.use_default_colors()

    curses.start_color()
    curses.init_pair(1, colors['black'], colors['green'])
    curses.init_pair(2, colors['white'], colors['default'])
    curses.init_pair(3, colors['green'], colors['default'])
    curses.init_pair(4, colors['blue'], colors['default'])

    while (k != ord('q')):

        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if height < 18 or width < 60:
            # catch small screen
            title = 'TERMINAL TO SMALL'
            c_y, c_x = int((height // 2) - 1), int((width // 2) - (len(title) // 2) - len(title) % 2)
            stdscr.addstr(c_y, c_x, title, curses.color_pair(3))

        else:
            # release, kernel
            # ------------------------------------------------------------------
            rel = sysinfo.rel()

            c_y, c_x = 0, 0
            stdscr.addstr(c_y, c_x, rel, curses.color_pair(2))

            # uptime, load average
            # ------------------------------------------------------------------
            upt = sysinfo.upt()

            c_y, c_x = 1, 0
            stdscr.addstr(c_y, c_x, upt, curses.color_pair(2))

            # cpu
            # ------------------------------------------------------------------
            cpu = sysinfo.cpu()

            c_y, c_x = c_y + 2, 0
            stdscr.addstr(c_y, c_x, 'CPU', curses.color_pair(2) | curses.A_BOLD)

            i = c_y + 1
            for item in cpu:
                c_y, c_x = i, 0
                add_unit(stdscr, c_y, c_x, item, item['name'], 'cpu')
                i = i + 1

            # ram
            # ------------------------------------------------------------------
            mem = sysinfo.mem()
            swp = sysinfo.swp()

            c_y, c_x = i + 1, 0
            stdscr.addstr(c_y, c_x, 'RAM', curses.color_pair(2) | curses.A_BOLD)

            c_y, c_x = c_y + 1, 0
            add_unit(stdscr, c_y, c_x, mem, 'memory', 'ram')

            c_y, c_x = c_y + 1, 0
            add_unit(stdscr, c_y, c_x, swp, 'swap', 'ram')

            # hdd
            # ------------------------------------------------------------------
            hdd = sysinfo.hdd()

            c_y, c_x = c_y + 2, 0
            stdscr.addstr(c_y, c_x, 'HDD', curses.color_pair(2) | curses.A_BOLD)

            j = c_y + 1
            for item in hdd:
                c_y, c_x = j, 0
                add_unit(stdscr, c_y, c_x, item, item['name'], 'hdd')
                j = j + 1

            # bottom info
            # ------------------------------------------------------------------
            bottom_info = "Press 'q' to exit"
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(height - 1, 0, bottom_info)
            stdscr.addstr(height - 1, len(bottom_info), " " * (width - len(bottom_info) - 1))
            stdscr.attroff(curses.color_pair(1))

        stdscr.timeout(1000) # 1 sec.
        stdscr.refresh()

        k = stdscr.getch()

def main():
    curses.wrapper(run)