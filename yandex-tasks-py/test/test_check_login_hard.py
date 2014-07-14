from login_check import check_login_hard as check_login
from unittest import TestCase


class TestCheckLoginHard(TestCase):
    def test_correct1(self):
        self.assertTrue(check_login("aaa"))

    def test_correct2(self):
        self.assertTrue(check_login("aaa9"))

    def test_correct3(self):
        self.assertTrue(check_login("aa.a"))

    def test_correct4(self):
        self.assertTrue(check_login("aa-a"))

    def test_correct5(self):
        self.assertTrue(check_login("aa.-a"))

    def test_correct6(self):
        self.assertTrue(check_login("a0123456789012345678"))

    def test_correct7(self):
        self.assertTrue(check_login("A"))

    def test_incorrect1(self):
        self.assertFalse(check_login("aa$aa"))

    def test_incorrect2(self):
        self.assertFalse(check_login("a."))

    def test_incorrect3(self):
        self.assertFalse(check_login("a-"))

    def test_incorrect4(self):
        self.assertFalse(check_login("a01234567890123456789a"))

    def test_incorrect4(self):
        self.assertFalse(check_login("."))