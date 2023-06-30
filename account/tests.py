from django.test import TestCase
from django.contrib.auth import authenticate, get_user_model
from django.db.utils import IntegrityError

User = get_user_model()


class A(TestCase):
    def test_auth001(self):
        user = authenticate(uid='a001001')
        self.assertIsInstance(user, User)

        user = authenticate(uid='a001001')
        self.assertIsInstance(user, User)

        user = authenticate(uid='b002002')
        self.assertIsInstance(user, User)

    def test_auth002(self):
        with self.assertRaises(Exception) as e:
            user = authenticate(uid='b001001')
            print(user)
        self.assertIsInstance(e.exception, Exception)

    def test_create_user_001(self):
        user = User.objects.create_user(
            uid='q2917013',
            division='フリーター',
            first_name='よこた',
            last_name='よしのり',
            email='yokota@yynet.org',
            is_staff=True,
            is_active=True,
            password='pswd0000',
        )
        self.assertIsInstance(user, User)

    def test_create_user_002(self):
        uid = 'q2917013'
        u0 = User.objects.create_user(uid=uid)
        self.assertIsInstance(u0, User)
        with self.assertRaises(Exception) as e:
            u1 = User.objects.create_user(uid=uid)
            self.assertIsInstance(u1, User)
        self.assertIsInstance(e.exception, IntegrityError)

    def test_create_superuser_001(self):
        user = User.objects.create_superuser(
            uid='q2917013',
            division='フリーター',
            first_name='よこた',
            last_name='よしのり',
            email='yokota@yynet.org',
            is_staff=True,
            is_active=True,
            password='pswd0000',
        )
        self.assertIsInstance(user, User)

    def test_create_superuser_002(self):
        uid = 'q2917013'
        u0 = User.objects.create_superuser(uid=uid)
        self.assertIsInstance(u0, User)
        with self.assertRaises(Exception) as e:
            u1 = User.objects.create_superuser(uid=uid)
            self.assertIsInstance(u1, User)
        self.assertIsInstance(e.exception, IntegrityError)
