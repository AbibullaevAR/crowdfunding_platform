import json
from dataclasses import dataclass, asdict

from django.conf import settings

from accounts.utilities import check_reg_token, RegTokenNotValid
from .helpers import UserEntity, UsersDAO


@dataclass
class EmailConfirmation:
    type_modification: str = 'email-confirm'
    is_confirm: bool = False


class ConfirmEmailService:

    def execute(self, token: str) -> str:

        email_confirmation = EmailConfirmation(type_modification='email-confirm', is_confirm=True)

        try:
            user_id = check_reg_token(token=token, max_age=24*3600)
        except (RegTokenNotValid):
            email_confirmation.is_confirm = False

        if email_confirmation.is_confirm:
            user_DAO = UsersDAO()
            user_entity: UserEntity = user_DAO.get_user_by_id(user_id=user_id)
            user_entity.is_active = True
            user_DAO.save_user(user_entity=user_entity)

        email_confirmation_json = json.dumps(asdict(email_confirmation))

        return settings.FRONTEND_URL + f'/user/modification?data={email_confirmation_json}'