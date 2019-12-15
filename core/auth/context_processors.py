from members.models import Member
import jwt


def member(request):
    if request.session.get('token', False):
        payload = jwt.decode(request.session.get('token'), audience='kerala_aud')
        user = Member.get_registered_member(payload)
        if user:
            return {'user': {"name": user.get_full_name(), 'id': str(user.id), "is_admin": user.is_admin,
                             "image": user.image.read() if user.image else ""}}
    return {}
