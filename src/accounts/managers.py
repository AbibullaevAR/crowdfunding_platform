from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        
        from .services import CreateUserService
        
        user = CreateUserService().execute(email, password, **extra_fields)

        return user

    def create_superuser(self, email, password, **extra_fields):
        pass