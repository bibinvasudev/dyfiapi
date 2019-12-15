from functools import wraps
from members.models import Member
import jwt
from jwt.exceptions import InvalidTokenError
from django.utils.decorators import available_attrs
from django.contrib.auth.views import redirect_to_login


class TokenAuthenticate(object):

    @classmethod
    def authenticate(cls, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            raise InvalidTokenError
        payload = jwt.decode(token, audience='kerala_aud')
        user = Member.get_registered_member(payload)
        request.user = user
        if not user:
            raise InvalidTokenError
        return user


def has_valid_token(view_func):
    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        from members.models import Member
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)

        if 'token' not in request.session:
            return redirect_to_login(request.get_full_path())

        payload = jwt.decode(request.session.get('token'), audience='kerala_aud')
        user = Member.get_registered_member(payload)
        request.user = {"name": user.get_full_name(), 'id': str(user.id), "is_admin": user.is_admin,
                        "image": user.image.read() if user.image else ""}
        return view_func(request, *args, **kwargs)
    return _wrapped_view

