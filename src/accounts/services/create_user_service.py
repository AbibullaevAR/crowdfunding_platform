
from django.contrib.auth import get_user_model

from .helpers import UserEntity, UsersDAO

UserModel = get_user_model()

class CreateUserService:


    def execute(self, password: str, **extra_fields) -> UserModel:

        user_DAO = UsersDAO()
        user_entity = user_DAO.create_user(password=password, **extra_fields)

        user_DAO.email_user(user_entity, 'resrt', 'test mgs')

        return user_DAO.entity_to_model(user_entity)


        