
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

from accounts.utilities import generate_reg_token
from .helpers import UserEntity, UsersDAO

UserModel = get_user_model()

class CreateUserService:


    def execute(self, password: str, view, **extra_fields) -> UserModel:

        user_DAO = UsersDAO()
        user_entity = user_DAO.create_user(password=password, is_active=False, **extra_fields)

        token = generate_reg_token(user_entity.id)

        url = settings.FRONTEND_URL + reverse('accounts:confirm_email',  kwargs={'token':token})

        user_DAO.email_user(
            user_entity, 
            'confirm email', 
            f'Click this link to confirm your email: {url}'
            )

        return user_DAO.entity_to_model(user_entity)


        