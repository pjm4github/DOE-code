import curses
import os


class Setup:
    def __init__(self):
        self.height = 0
        self.width = 0
        self.status = "Ready"
        self.blank = [0]*1024

    def edit_bool(self, row, col, length, prop):
        pass

    def edit_in_place(self, row, col, length, prop):
        pass

    def edit_globals(self):
        i = 0
        var = None
        nvars = 0
        nsize = 0
        if var is None:
            pass
        first = 0
        sel = 0
        vsize = self.height - 5
        last = first + vsize
        if last >= nvars:
            last = int(nvars-1)
        row = 4
        for i in range(first, last):
            value = [0]*1024
            if global_getvar(var[i].prop.name, value, len(value)):
                v = value
                if v[0] == '\'' or v[0] == '\"':
                    pass
                selected = (i == sel)
                if selected:
                    pass
                print(row, nsize+1, "%-*s" % (self.width-nsize-1, v))
                if selected:
                    pass
        key = 0
        while (key := wgetch(stdscr)) == ERR:
            pass
        if key == KEY_DOWN:
            if sel < nvars-2:
                sel += 1
                if sel >= last and first < nvars-vsize-1:
                    first += 1
        elif key == KEY_UP:
            if sel > 0:
                sel -= 1
                if sel < first:
                    first = sel
        elif key == KEY_ENTER:
            if var[sel].prop.access == PA_PUBLIC:
                self.edit_in_place(4+sel-first, nsize+1, self.width-nsize-1, var[sel].prop)
        else:
            pass
        if var[sel].prop.access == PA_PUBLIC:
            self.status = "Hit <Return> to edit this variable."
        else:
            self.status = "This variable cannot be changed."
        return key

    def edit_environment(self):
        pass

    def edit_macros(self):
        pass

    def edit_config(self):
        pass

    def show_help(self):
        pass

    def do_quit(self):
        pass


class SETUPGROUP:
    def __init__(self, name, edit):
        self.name = name
        self.edit = edit


def setup():
    from curses import initscr, halfdelay, clear, ERR, wgetch, KEY_DOWN, KEY_UP, KEY_ENTER, stdscr, loadall

    if not loadall(None):
        status = "ERROR: unable to load configuration files"
    done = False
    tab = 0
    group = [SETUPGROUP("Globals", Setup.edit_globals),
             SETUPGROUP("Environment", Setup.edit_environment),
             SETUPGROUP("Macros", Setup.edit_macros),
             SETUPGROUP("Config", Setup.edit_config)]
    initscr()
    halfdelay(1)
    clear()
    width = 0
    for i in range(width):
        blank[i] = ' '
    blank[i] = '\0'
    while not done:
        pass

    return 0


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def edit_bool(row, col, length, prop):
    value = False
    string = [''] * 1024
    while True:
        key = stdscr.getch()
        if key == KEY_ENTER:
            break
        if key == KEY_ESC:
            return False
        if key in ['Y', 'T', '1', KEY_DOWN]:
            value = True
        if key in ['N', 'F', '0', KEY_UP]:
            value = False
        if convert_from_boolean(string, len(string), value, prop):
            stdscr.addstr(row, col, f"{string[:length]}")
    return value


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def edit_in_place(row, col, length, prop):
    stdscr.addstr(row, col-1, "[")
    if prop.width > 0 and prop.width < length:
        length = prop.width
    if col + length > width - 2:
        length = width - 2 - col
    stdscr.addstr(row, col + length + 1, "]")
    while True:
        key = stdscr.getch()
        if key == KEY_ESC:
            return False
        elif key == KEY_ENTER:
            return True


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def edit_environment():
    key = 0
    while key == -1:
        key = stdscr.getch()
    # TODO handle input locally
    return key  # pass up for global input handling, 0 does nothing

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def edit_macros():
    key = 0
    while (key = stdscr.getch()) == ERR:
        pass
    # TODO handle input locally
    return key  # pass up for global input handling, 0 does nothing

def edit_config():
    key = None
    while key is None:
        key = stdscr.getch()
    # TODO handle input locally
    return key  # pass up for global input handling, 0 does nothing

def show_help():
    while curses.wgetch(curses.stdscr) == curses.ERR:
        pass


def do_quit():
    fname = "gridlabd-{}.conf".format(os.getenv("USER"))
    print("Save to '{}' (Y/N)? [Y]".format(fname))
    return True
