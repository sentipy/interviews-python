import array
import sys
import os
import multiprocessing
import heapq
import collections
import resource

MAX_MEMORY_ALLOWED = 256 * 1024 * 1024


def set_limits(div):
    resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY_ALLOWED // div, MAX_MEMORY_ALLOWED // div))
    resource.setrlimit(resource.RLIMIT_DATA, (MAX_MEMORY_ALLOWED // div, MAX_MEMORY_ALLOWED // div))
    resource.setrlimit(resource.RLIMIT_MEMLOCK, (MAX_MEMORY_ALLOWED // div, MAX_MEMORY_ALLOWED // div))


def process_init():
    """
    initialize procedure for every process
    """
    set_limits(1)


def get_array_type():
    """
    detecting type of array to store 4-byte unsigned integers
    """
    tmp = array.array('I')
    tmp.append(1)
    tmp.byteswap()
    return 'I' if len(bin(tmp[0])) == 27 else 'L'


def is_need_to_swap_bytes():
    return sys.byteorder == 'little'


class FileReader:
    """
    class which takes care of reading file and providing integers
    without necessity of thinking of endianness (big or little).
    Also treats itself as an iterator for convenience
    """

    def __init__(self, file, mode, arr_type, swap_bytes, max_memory):
        self.file = open(file, mode)
        self.swap_bytes = swap_bytes
        self.ints_left_in_file = os.path.getsize(file) // 4
        self.max_memory = max_memory
        self.arr = array.array(arr_type)
        self.read_from_file()
        self.file.__enter__()

    def read_from_file(self):
        if self.ints_left_in_file > 0:
            self.arr.fromfile(self.file, min(self.max_memory // 4, self.ints_left_in_file))
            self.ints_left_in_file -= len(self.arr)
            if self.swap_bytes:
                self.arr.byteswap()
            self.deque = collections.deque(iter(self.arr))
            del self.arr[:]

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.__exit__(exc_type, exc_val, exc_tb)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.deque.popleft()
        except IndexError:
            pass
        self.read_from_file()
        try:
            return self.deque.popleft()
        except IndexError:
            pass
        raise StopIteration


class FileMerger:
    def __init__(self):
        self.arr_type = get_array_type()
        self.is_need_swap = is_need_to_swap_bytes()

    def merge(self, file1, file2, result_file, max_memory_allowed):
        with open(result_file, 'wb') as rf:
            fr1 = FileReader(file1, 'rb', self.arr_type, self.is_need_swap, max_memory_allowed // 2)
            fr2 = FileReader(file2, 'rb', self.arr_type, self.is_need_swap, max_memory_allowed // 2)
            with fr1:
                with fr2:
                    for i in heapq.merge(iter(fr1), iter(fr2)):
                        rf.write(i.to_bytes(4, 'big'))


def sort_and_write_to_file(arr, filename):
    arr.byteswap()
    sorted_list = sorted(arr)
    arr = array.array(get_array_type())
    arr.fromlist(sorted_list)
    arr.byteswap()
    with open(filename, 'wb') as nf:
        arr.tofile(nf)
    return filename


def merger_finish(new_files, filename1, filename2, result_filename):
    """
    procedure to call after finishing of file merging
    """

    def inner(_):
        new_files.append(result_filename)
        os.remove(filename1)
        os.remove(filename2)

    return inner


def sort_file(file_loc, output_filename):
    cpu_count = multiprocessing.cpu_count()
    size = os.path.getsize(file_loc)
    integers_left_to_read = size // 4
    max_read_at_once = MAX_MEMORY_ALLOWED // 4
    pool = multiprocessing.Pool(cpu_count, process_init)
    next_file_id = 0
    files = []
    fm = FileMerger()
    with open(file_loc, 'rb') as fl:
        while integers_left_to_read > 0:
            a = array.array(get_array_type())
            a.fromfile(fl, min(integers_left_to_read, max_read_at_once))
            next_file_id += 1
            pool.apply_async(sort_and_write_to_file, [a, 'tmp' + str(next_file_id) + '.txt'], callback=files.append)
            integers_left_to_read -= max_read_at_once
        pool.close()
        pool.join()
        files_count = len(files)
        while files_count > 1:
            pool = multiprocessing.Pool(cpu_count)
            new_files = []
            for i in range(files_count // 2):
                next_file_id += 1
                pool.apply_async(fm.merge,
                                 [files[2 * i], files[2 * i + 1], 'tmp' + str(next_file_id) + '.txt',
                                  MAX_MEMORY_ALLOWED // min(cpu_count, files_count)],
                                 #MAX_MEMORY_ALLOWED],
                                 callback=merger_finish(new_files, files[2 * i], files[2 * i + 1],
                                                        'tmp' + str(next_file_id) + '.txt'))
            pool.close()
            pool.join()
            if files_count & 1 == 1:
                new_files.append(files[-1])
            files = new_files
            files_count = len(files)
    os.rename(files[0], output_filename)


def is_file_sorted(filename, result_filename):
    with open(filename, 'rb') as f:
        with open(result_filename, 'rb') as fr:
            arr1 = array.array(get_array_type())
            arr2 = array.array(get_array_type())
            arr1.fromfile(f, os.path.getsize(filename) // 4)
            arr2.fromfile(fr, os.path.getsize(result_filename) // 4)
            if is_need_to_swap_bytes():
                arr1.byteswap()
                arr2.byteswap()
            sorted_arr = sorted(arr1)
            return sorted_arr == list(arr2)


if __name__ == '__main__':
    set_limits(1)
    if len(sys.argv) < 3:
        print('usage: ext_file_sort.py src_file dst_file')
        exit(0)
    sort_file(sys.argv[1], sys.argv[2])
    assert is_file_sorted(sys.argv[1], sys.argv[2])