# -*- coding: utf-8 -*-
from django.test import TestCase # noqa: F401,E261
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class A(TestCase):
    def test_a(self):
        uid = 'q2917013'
        user = User.objects.create_user(uid=uid)
        user.action.setIn()
        user.action.save()
        self.assertEqual(user.action.getStat(), '出社')
        user.action.setOut()
        user.action.save()
        self.assertEqual(user.action.getStat(), '退出')
        user.action.setIn(False)
        user.action.save()
        self.assertEqual(user.action.getStat(), '出社*')
        user.action.setOut(False)
        user.action.save()
        self.assertEqual(user.action.getStat(), '退出*')
