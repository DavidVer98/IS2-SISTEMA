import unittest

from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase
from django.utils.datetime_safe import date


class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get('127.0.0.1:8000')
        self.assertEqual(response.status_code, 404)


class SigninTest(TestCase):

    def test_correct(self):
        user = authenticate(username='elias', password='admin')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)
#
    def test_wrong_pssword(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)

class TestBasic(unittest.TestCase):
    "Basic tests"

    def test_basic(self):
        a = 1
        self.assertEqual(1, a)

    def test_basic_2(self):
        a = 1
        assert a == 1



