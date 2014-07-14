from unittest import TestCase
from create_dict import create_dict


class TestCreateDict(TestCase):
    def test_create_dict_equal(self):
        list_keys = [1, 2, 'a', 'b']
        list_values = ['a', 'b', 1, 2]
        d = create_dict(list_keys, list_values)
        for i in (range(len(list_keys))):
            self.assertTrue(list_keys[i] in d, 'Key ' + str(list_keys[i]) + ' not found')
            self.assertTrue(d.get(list_keys[i]) == list_values[i],
                            'Value for key ' + str(list_keys[i]) + ' is incorrect')

    def test_create_dict_less_keys(self):
        list_keys = [1, 2, 'a']
        list_values = ['a', 'b', 1, 2]
        d = create_dict(list_keys, list_values)
        for i in (range(len(list_keys))):
            self.assertTrue(list_keys[i] in d, 'Key ' + str(list_keys[i]) + ' not found')
            self.assertTrue(d.get(list_keys[i]) == list_values[i],
                            'Value for key ' + str(list_keys[i]) + ' is incorrect')

    def test_create_dict_equal_more_keys(self):
        list_keys = [1, 2, 'a', 'b']
        list_values = ['a', 'b', 1]
        d = create_dict(list_keys, list_values)
        for i in (range(len(list_values))):
            self.assertTrue(list_keys[i] in d, 'Key ' + str(list_keys[i]) + ' not found')
            self.assertTrue(d.get(list_keys[i]) == list_values[i],
                            'Value for key ' + str(list_keys[i]) + ' is incorrect')
        i = len(list_values)
        while i < len(list_keys):
            self.assertTrue(list_keys[i] in d, 'Key ' + str(list_keys[i]) + ' not found')
            self.assertTrue(d.get(list_keys[i]) is None, 'Value for key ' + str(list_keys[i]) + ' must be None')
            i += 1