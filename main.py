#! /usr/bin/python

import sys
import curses

import info


def add_unit(stdscr, c_y, c_x, u_data, u_title, u_type):
    # Example:
    # unit1  [=========================] 15%  1.8G/11.7G
    # unit2  [=========================] 0%   0K/22.9G

    if u_type == 'cpu':
        # title
        stdscr.addstr(c_y, c_x, u_title)
        # status bar
        c_x = c_x + 8
        stdscr.addstr(c_y, c_x, '[')
        c_x = c_x + 1
        perc = int(u_data['used'])
        st_bar_len = 25
        st_bar_used = (st_bar_len * perc) / 100
        st_bar_free = st_bar_len - st_bar_used
        if st_bar_used == 0:
            stdscr.addstr(c_y, c_x, '=' * st_bar_free, curses.color_pair(3) | curses.A_BOLD)
        else:
            stdscr.addstr(c_y, c_x, '=' * st_bar_used, curses.color_pair(4) | curses.A_BOLD)
            stdscr.addstr(c_y, c_x + st_bar_used, '=' * st_bar_free, curses.color_pair(3) | curses.A_BOLD)
        c_x = c_x + st_bar_len
        stdscr.addstr(c_y, c_x, ']')
        # used %
        c_x = c_x + 2
        stdscr.addstr(c_y, c_x, str(perc) + '%', curses.color_pair(4))

    if u_type == 'ram' or u_type == 'hdd':
        # title
        stdscr.addstr(c_y, c_x, u_title)
        # status bar
        c_x = c_x + 8
        stdscr.addstr(c_y, c_x, '[')
        c_x = c_x + 1
        perc = int((float(u_data['used']) / float(u_data['size'])) * 100)
        st_bar_len = 25
        st_bar_used = (st_bar_len * perc) / 100
        st_bar_free = st_bar_len - st_bar_used
        if st_bar_used == 0:
            stdscr.addstr(c_y, c_x, '=' * st_bar_free, curses.color_pair(3) | curses.A_BOLD)
        else:
            stdscr.addstr(c_y, c_x, '=' * st_bar_used, curses.color_pair(4) | curses.A_BOLD)
            stdscr.addstr(c_y, c_x + st_bar_used, '=' * st_bar_free, curses.color_pair(3) | curses.A_BOLD)
        c_x = c_x + st_bar_len
        stdscr.addstr(c_y, c_x, ']')
        # used %
        c_x = c_x + 2
        stdscr.addstr(c_y, c_x, str(perc) + '%', curses.color_pair(4))
        # used
        c_x = c_x + 5
        stdscr.addstr(c_y, c_x, u_data['used'] + u_data['used_f'], curses.color_pair(3))
        # size
        c_x = c_x + len(u_data['used'] + u_data['used_f'])
        stdscr.addstr(c_y, c_x, '/' + u_data['size'] + u_data['size_f'], curses.color_pair(3))

def main(stdscr):
    k = 0

    stdscr.clear()
    stdscr.refresh()

    curses.curs_set(0)
    curses.use_default_colors()

    curses.start_color()
    curses.init_pair(1, 0,  2) # bottom help info
    curses.init_pair(2, 2, -1) # CPU, RAM, HDD title
    curses.init_pair(3, 8, -1) # status bar '-'
    curses.init_pair(4, 2, -1) # status bar '+'

    while (k != ord('q')):

        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if height < 20 or width < 60:
            # catch small screen
            title = 'TERMINAL TO SAMLL'
            c_y, c_x = int((height // 2) - 1), int((width // 2) - (len(title) // 2) - len(title) % 2)
            stdscr.addstr(c_y, c_x, title, curses.color_pair(2))

        else:
            # release & kernel
            # ----------------------------------------------------------------------
            c_y, c_x = 0, 0
            lsb = info.lsb()
            stdscr.addstr(c_y, c_x, lsb, curses.color_pair(2))

            # uptime & load average
            # ----------------------------------------------------------------------
            c_y, c_x = 1, 0
            upt = info.upt()
            stdscr.addstr(c_y, c_x, upt, curses.color_pair(3))

            # cpu
            # ----------------------------------------------------------------------
            c_y, c_x = c_y + 2, 0
            stdscr.addstr(c_y, c_x, 'CPU', curses.color_pair(2) | curses.A_BOLD)
            cpu = info.cpu()
            i = c_y + 1
            for item in cpu:
                c_y, c_x = i, 0
                add_unit(stdscr, c_y, c_x, item, item['name'], 'cpu')
                i = i + 1

            # ram
            # ----------------------------------------------------------------------
            c_y, c_x = i + 1, 0
            stdscr.addstr(c_y, c_x, 'RAM', curses.color_pair(2) | curses.A_BOLD)

            c_y, c_x = c_y + 1, 0
            mem = info.mem()
            add_unit(stdscr, c_y, c_x, mem, 'memory', 'ram')

            c_y, c_x = c_y + 1, 0
            swp = info.swp()
            add_unit(stdscr, c_y, c_x, swp, 'swap', 'ram')

            # hdd
            # ----------------------------------------------------------------------
            c_y, c_x = c_y + 2, 0
            stdscr.addstr(c_y, c_x, 'HDD', curses.color_pair(2) | curses.A_BOLD)

            hdd = info.hdd()
            j = c_y + 1
            for item in hdd:
                c_y, c_x = j, 0
                add_unit(stdscr, c_y, c_x, item, item['name'], 'hdd')
                j = j + 1

            # bottom info
            # ----------------------------------------------------------------------
            bottom_info = "Press 'q' to exit"
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(height - 1, 0, bottom_info)
            stdscr.addstr(height - 1, len(bottom_info), " " * (width - len(bottom_info) - 1))
            stdscr.attroff(curses.color_pair(1))

        stdscr.timeout(1000) # 1 sec.
        stdscr.refresh()

        k = stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)