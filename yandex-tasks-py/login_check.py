import re

global comp1
comp1 = re.compile("[A-Za-z]\Z")
global comp
comp = re.compile("[A-Za-z][A-Za-z0-9\.-]{0,18}[A-Za-z0-9]\Z")


def check_login(login):
    len_login = len(login)
    if len_login < 1:
        return False
    if len_login == 1:
        cur_comp = comp1
    else:
        cur_comp = comp
    if cur_comp.match(login):
        return True
    return False


def check_login_hard(login):
    len_login = len(login)
    if len_login < 1 or len_login > 20:
        return False
    if login[0].isalpha():
        i = 1
        while i < len_login - 1:
            ch = login[i]
            if not (ch.isalpha() or ch.isdigit() or ch == '.' or ch == '-'):
                return False
            i += 1
        ch = login[len_login - 1]
        if ch.isalpha() or ch.isdigit():
            return True
    return False