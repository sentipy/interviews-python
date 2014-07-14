from create_dict import *
from login_check import *
import timeit


"""list_keys8 = list()
list_values8 = list()
for i in range(8 * 1000 * 1000):
    list_keys8.append(i)
    list_values8.append(i)

list_keys1 = list()
list_values1 = list()
for i in range(8 * 1000 * 1000):
    list_keys1.append(i)
    list_values1.append(i)

times = 2

T_1 = timeit.timeit('create_dict_loop(list_keys8, list_values8)',
                   setup="from __main__ import create_dict_loop, list_keys8, list_values8", number=times)
print(T_1)
T1_2 = timeit.timeit('create_dict(list_keys8, list_values8)',
                   setup="from __main__ import create_dict, list_keys8, list_values8", number=times)
print(T1_2)
T1_3 = timeit.timeit('create_dict(list_keys1, list_values8)',
                   setup="from __main__ import create_dict, list_keys1, list_values8", number=times)
print(T1_3)
T1_4 = timeit.timeit('create_dict(list_keys8, list_values1)',
                   setup="from __main__ import create_dict, list_keys8, list_values1", number=times)
print(T1_4)"""

times = 1000000

T2_1 = timeit.timeit("check_login('abc.123')",
                   setup="from __main__ import check_login", number=times)
print(T2_1)

T2_2 = timeit.timeit("check_login_hard('abc.123')",
                   setup="from __main__ import check_login_hard", number=times)
print(T2_2)