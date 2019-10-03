from members.models import Member
import jwt
from jwt.exceptions import InvalidTokenError


class TokenAuthenticate(object):

    @classmethod
    def authenticate(cls, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            raise InvalidTokenError
        payload = jwt.decode(token, audience='kerala_aud')
        user = Member.get_registered_member(payload)
        if not user:
            raise InvalidTokenError
        return user

