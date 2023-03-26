
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

class RegTokenNotValid(Exception):
    pass


def generate_reg_token(user_id: str) -> str:
    signer = TimestampSigner()
    return signer.sign_object(user_id)


def check_reg_token(token: str, max_age: int) -> int:
    signer = TimestampSigner()

    try:
        user_id = signer.unsign_object(token, max_age=max_age)

    except (BadSignature, SignatureExpired):
        raise RegTokenNotValid()
    
    return user_id



