import struct
import array
import random
import os
import time
import multiprocessing
import numpy

MAX_MEMORY_ALLOWED = 16


def sort_and_write_to_file(arr, id_file):
    arr.byteswap()
    #lst = arr.tolist()
    #s = sorted(lst)
    sorted_list = sorted(arr)
    arr = array.array('I')
    arr.fromlist(sorted_list)
    arr.byteswap()
    filename = 'tmp' + str(id_file) + '.txt'
    with open(filename, 'wb') as nf:
        arr.tofile(nf)
    return filename


def merge_files(filename1, filename2, id_file, max_memory):
    print("merging " + filename1 + " and " + filename2 + " new:" + str(id_file))
    filename = 'tmp' + str(id_file) + '.txt'
    ints_left_in_file1 = os.path.getsize(filename1) // 4
    ints_left_in_file2 = os.path.getsize(filename2) // 4
    max_ints_from_file1 = max_memory // 4 // 4
    max_ints_from_file2 = max_memory // 4 // 4
    max_ints_in_temp_array = max_memory // 4 - max_ints_from_file1 - max_ints_from_file2
    with open(filename, 'wb') as nf:
        with open(filename1, 'rb') as f1:
            with open(filename2, 'rb') as f2:
                tmp_arr = array.array('I')
                elements_in_temp_array = 0
                arr1 = array.array('I')
                arr2 = array.array('I')
                while ints_left_in_file1 > 0 and ints_left_in_file2 > 0:
                    if len(arr1) == 0:
                        arr1.fromfile(f1, min(ints_left_in_file1, max_ints_from_file1))
                        #arr1.byteswap()
                        ints_left_in_file1 -= max_ints_from_file1
                    if len(arr2) == 0:
                        arr2.fromfile(f2, min(ints_left_in_file2, max_ints_from_file2))
                        #arr2.byteswap()
                        ints_left_in_file2 -= max_ints_from_file2
                    while len(arr1) > 0 and len(arr2) > 0 and elements_in_temp_array < max_ints_in_temp_array:
                        if arr1[0] < arr2[0]:
                            tmp_arr.append(arr1.pop())
                        else:
                            tmp_arr.append(arr2.pop())
                        elements_in_temp_array += 1
                        print(tmp_arr)
                    if elements_in_temp_array == max_ints_in_temp_array:
                        tmp_arr.byteswap()
                        tmp_arr.tofile(nf)
                        tmp_arr = array.array('I')
                        elements_in_temp_array = 0
                tmp_arr.byteswap()
                print(tmp_arr)
                tmp_arr.tofile(nf)
                arr1.tofile(nf)
                arr2.tofile(nf)
                max_ints = max_memory // 4
                while ints_left_in_file1 > 0:
                    tmp_arr = array.array('I')
                    tmp_arr.fromfile(f1, min(ints_left_in_file1, max_ints))
                    ints_left_in_file1 -= max_ints
                    tmp_arr.tofile(nf)
                while ints_left_in_file2 > 0:
                    tmp_arr = array.array('I')
                    tmp_arr.fromfile(f2, min(ints_left_in_file2, max_ints))
                    ints_left_in_file2 -= max_ints
                    tmp_arr.tofile(nf)
    return filename


def sort_file(file_loc):
    cpu_count = multiprocessing.cpu_count()
    size = os.path.getsize(file_loc)
    integers_left_to_read = size // 4
    max_read_at_once = MAX_MEMORY_ALLOWED // 4
    pool = multiprocessing.Pool(cpu_count - 1)
    last_file_id = 0
    files = []
    with open(file_loc, 'rb') as fl:
        #b = f.read(4)
        #i, = struct.unpack('i', b)
        #print(i)
        while integers_left_to_read > 0:
            a = array.array('I')
            a.fromfile(fl, min(integers_left_to_read, max_read_at_once))
            last_file_id += 1
            pool.apply_async(sort_and_write_to_file, [a, last_file_id], callback=files.append)
            integers_left_to_read -= max_read_at_once
        while len(files) != last_file_id:
            pass
        files_count = len(files)
        while files_count > 1:
            new_files = []
            for i in range(files_count // 2):
                last_file_id += 1
                pool.apply_async(merge_files, [files[2 * i], files[2 * i + 1], last_file_id, 8 * 1024 * 1024],
                                 callback=new_files.append)
            while len(new_files) != files_count // 2:
                pass
            files = new_files
            files_count = len(files)


n = 384 * 1024 * 1024 // 4
n = 4 * 1024 // 4
#n = 3
gen = True
#gen = False

if gen:
    with open('4k.txt', 'wb') as f:
        random.seed()
        for _ in range(n):
            r = random.randint(0, 2 << 30)
            f.write(r.to_bytes(4, 'big'))

t1 = time.time()
#sort_file('32mb.txt')
#sort_file('37.txt')
t2 = time.time()
print(t2 - t1)
