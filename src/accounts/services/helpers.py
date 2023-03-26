from dataclasses import dataclass, asdict

from django.contrib.auth import get_user_model


UserModel = get_user_model()

@dataclass
class UserEntity:
    id: int
    email: str
    is_active: bool
    is_admin: bool


class UsersDAO:

    def orm_to_entity(self, user_orm: UserModel) -> UserEntity:     
        return UserEntity(         
            id=user_orm.id,         
            email=user_orm.email,
            is_active=user_orm.is_active,
            is_admin=user_orm.is_admin 
        )
    
    def entity_to_model(self, user_entity: UserEntity) -> UserModel:
        return UserModel.objects.get(pk=user_entity.pk)

    def create_user(self, password: str, **extra_fields) -> UserEntity:

        user = UserModel(**extra_fields)
        user.set_password(password)
        user.save()

        user_entity = self.orm_to_entity(user_orm=user)
        return user_entity
    
    def email_user(self, user_entity: UserEntity, subject: str, message: str, from_email=None, **kwargs) -> None:
        self.entity_to_model(user_entity).email_user(subject, message, from_email, **kwargs)
