from django.contrib.auth.hashers import make_password
from django.test import TestCase
from granite.models import CustomUser
from django.contrib.auth import authenticate
from django.test import Client


# Create your tests here.

class CustomUsertest(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(first_name='user123', last_name='last1', email='user123@gmail.com',
                                       password='pass123')
        CustomUser.objects.create_user(first_name='user456', last_name='last4', email='456u@gamil.com',
                                       password='pass456')
        self.user_pass = CustomUser.objects.create_user(email='peter@parker.com', password='peterparker')
        self.super = CustomUser.objects.create_superuser(email="super@user.com", password="superuser")

    def test_users(self):
        user1 = CustomUser.objects.get(first_name='user123')
        user2 = CustomUser.objects.get(first_name='user456')
        user3 = CustomUser.objects.filter(first_name='user123').exists()
        checkpass = self.user_pass.check_password("peterparker")
        super1 = CustomUser.objects.get(email="super@user.com")
        super_pass = self.super.check_password("superuser")
        self.assertEqual(user1.first_name, "user123")
        self.assertEqual(user2.first_name, "user456")
        self.assertTrue(user3)
        self.assertTrue(checkpass)
        self.assertEqual(super1.email, "super@user.com")
        self.assertTrue(super_pass)

