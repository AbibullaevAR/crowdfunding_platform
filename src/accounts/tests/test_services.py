from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.conf import settings

from accounts.services.helpers import UsersDAO, UserEntity
from accounts.services.create_user_service import CreateUserService
from accounts.services.confirm_email_service import ConfirmEmailService
from accounts.utilities import RegTokenNotValid

class CreateUserViewMock:

    def get_absolute_uri(self, local_url: str, **kwargs):
        pass

class CreateUserTestCase(TestCase):
    @patch.object(CreateUserViewMock, 'get_absolute_uri')
    @patch('accounts.services.create_user_service.generate_reg_token')
    @patch.object(UsersDAO, 'entity_to_model')
    @patch.object(UsersDAO, 'email_user')
    @patch.object(UsersDAO, 'create_user')
    def test_create_user(self, 
            create_user_mock: MagicMock, 
            email_user_mock: MagicMock, 
            entity_to_model_mock: MagicMock, 
            generate_reg_token_mock: MagicMock, 
            get_absolute_uri_mock: MagicMock
        ):

        user_entity = UserEntity(         
            id='adb753df-e64a-420e-b08e-164d008b9797',         
            email='test@mail.ru',
            is_active=False,
            is_admin=False
        )

        create_user_mock.return_value = user_entity
        email_user_mock.return_value = None
        entity_to_model_mock.return_value = 'UserModel'
        generate_reg_token_mock.return_value = 'token'
        get_absolute_uri_mock.return_value = 'absolute_uri'
        
        execute_value = CreateUserService().execute(
            password='123test',
            view=CreateUserViewMock(),
            email='test@mail.ru',
            name='test name'
        )

        assert execute_value == 'UserModel'

        create_user_mock.assert_called_once_with(
            password='123test',
            email='test@mail.ru',
            name='test name',
            is_active=False
        )
        email_user_mock.assert_called_once_with(
            user_entity,
            'confirm email',
            'Click this link to confirm your email: absolute_uri'
        )
        entity_to_model_mock.assert_called_once_with(user_entity)
        generate_reg_token_mock.assert_called_once_with(user_entity.id)
        get_absolute_uri_mock.assert_called_once_with('accounts:confirm_email', token='token')


class ConfirmEmailServiceTestCase(TestCase):
    @patch('accounts.services.confirm_email_service.check_reg_token')
    @patch.object(UsersDAO, 'get_user_by_id')
    @patch.object(UsersDAO, 'save_user')
    def test_confirm_email_valid_token(
            self,
            mock_save_user: MagicMock,
            mock_get_user_by_id: MagicMock,
            mock_check_reg_token: MagicMock
        ):

        user_entity = UserEntity(         
            id='adb753df-e64a-420e-b08e-164d008b9797',         
            email='test@mail.ru',
            is_active=False,
            is_admin=False
        )

        token = 'token'

        mock_save_user.return_value = None
        mock_check_reg_token.return_value = user_entity.id
        mock_get_user_by_id.return_value = user_entity

        return_value = ConfirmEmailService().execute(token)

        assert return_value == settings.FRONTEND_URL + '/user/modification?data={"type_modification": "email-confirm", "is_confirm": true}'

        mock_check_reg_token.assert_called_once_with(token=token, max_age=24*3600)
        mock_get_user_by_id.assert_called_once_with(user_id=user_entity.id)
        mock_save_user.assert_called_once_with(user_entity=user_entity)

    @patch('accounts.services.confirm_email_service.check_reg_token', MagicMock(side_effect=RegTokenNotValid()))
    @patch.object(UsersDAO, 'get_user_by_id')
    @patch.object(UsersDAO, 'save_user')
    def test_confirm_email_not_valid_token(
            self,
            mock_save_user: MagicMock,
            mock_get_user_by_id: MagicMock,
        ):

        user_entity = UserEntity(         
            id='adb753df-e64a-420e-b08e-164d008b9797',         
            email='test@mail.ru',
            is_active=False,
            is_admin=False
        )

        token = 'token'

        mock_save_user.return_value = None
        mock_get_user_by_id.return_value = user_entity

        return_value = ConfirmEmailService().execute(token)

        assert return_value == settings.FRONTEND_URL + '/user/modification?data={"type_modification": "email-confirm", "is_confirm": false}'

        mock_save_user.assert_not_called()
        mock_get_user_by_id.assert_not_called()
        