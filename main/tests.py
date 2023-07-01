# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

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


class B(TestCase):
    def setUp(self):
        self.client = Client()

    def test_a(self):
        u = ['q2917013', 'q1239874', 'qa9932022']
        for _ in u:
            user = User.objects.create_user(uid=_)
            user.action.setIn()
            user.action.save()

        r = self.client.get(reverse('main:top'))
        self.assertEqual(r.status_code, 200)
        self.assertIn('form', r.context)
        self.assertEqual(len(r.context['form'].fields), len(u))
        for i, f in enumerate(r.context['form'].fields):
            self.assertEqual(f, 'cb_' + u[i])

    def test_b(self):
        u = ['q2917013', 'q1239874', 'qa9932022']
        for _ in u:
            user = User.objects.create_user(uid=_)
            user.action.setIn()
            user.action.save()
        self.assertEqual(len(u), len(User.objects.all()))
        for user in User.objects.all():
            self.assertEqual(user.action.getStat(), '出社')

        op = {}
        for _ in u:
            op.update({'cb_' + _: True})

        r = self.client.post(reverse('main:top'), op)
        self.assertRedirects(r, reverse('main:top'))

        for user in User.objects.all():
            self.assertEqual(user.action.getStat(), '退出')
