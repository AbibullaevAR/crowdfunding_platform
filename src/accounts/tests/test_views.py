from unittest.mock import patch, MagicMock

from django.conf import settings
from django.core import mail
from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.views import CreateUserView, ConfirmEmailView
from accounts.utilities import generate_reg_token

class CreateUserViewTestCase(TestCase):
    
    def test_create_user_view_valid_data(self):

        resp = self.client.post(reverse('accounts:create_user'), data={'name': 'test name', 'email': 'test@mail.ru', 'password': 'test'})
        
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.resolver_match.func.__name__, CreateUserView.as_view().__name__)

        create_user = get_user_model().objects.first()

        self.assertIsNotNone(create_user)
        self.assertEqual(create_user.name, 'test name')
        self.assertEqual(create_user.email, 'test@mail.ru')
        self.assertFalse(create_user.is_admin)
        self.assertFalse(create_user.is_active)
        self.assertTrue(create_user.check_password('test'))

        self.assertEqual(len(mail.outbox), 1)
    
    def test_create_user_not_valid_data(self):
        resp = self.client.post(reverse('accounts:create_user'), data={'name': 'test name', 'email': 'testmail.ru', 'password': 'test'})
        
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.resolver_match.func.__name__, CreateUserView.as_view().__name__)

        create_user = get_user_model().objects.first()

        self.assertIsNone(create_user)

        self.assertEqual(len(mail.outbox), 0)


class ConfirmEmailViewTestCase(TransactionTestCase):

    User = get_user_model()

    def setUp(self):
        user = self.User.objects.create(name='test name', email = 'test@mail.ru', is_active=False)
        user.set_password('test')
        user.save()

    def test_confirm_email_valid_token(self):
        token = generate_reg_token(str(self.User.objects.first().id))

        resp = self.client.get(reverse('accounts:confirm_email', kwargs={'token':token}))
        
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.resolver_match.func.__name__, ConfirmEmailView.as_view().__name__)
        self.assertEqual(resp.url, settings.FRONTEND_URL + '/user/modification?data=%7B%22type_modification%22:%20%22email-confirm%22,%20%22is_confirm%22:%20true%7D')      

        user = self.User.objects.first()

        self.assertTrue(user.is_active)
        self.assertEqual(user.name, 'test name')
        self.assertEqual(user.email, 'test@mail.ru')
        self.assertTrue(user.check_password('test'))
        self.assertFalse(user.is_admin)
    
    def test_confirm_email_not_valid_token(self):
        token = 'not valid token'

        resp = self.client.get(reverse('accounts:confirm_email', kwargs={'token':token}))
        
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.resolver_match.func.__name__, ConfirmEmailView.as_view().__name__)
        self.assertEqual(resp.url, settings.FRONTEND_URL + '/user/modification?data=%7B%22type_modification%22:%20%22email-confirm%22,%20%22is_confirm%22:%20false%7D')    

        user = self.User.objects.first()  

        self.assertFalse(user.is_active)
        self.assertEqual(user.name, 'test name')
        self.assertEqual(user.email, 'test@mail.ru')
        self.assertTrue(user.check_password('test'))
        self.assertFalse(user.is_admin)