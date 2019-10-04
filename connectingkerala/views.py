from django.conf import settings
from members.models import Member
from core.helpers import Helper
import jwt
from core.response import HTTPResponse
from rest_framework import viewsets
from rest_framework import status


class LoginView(viewsets.GenericViewSet):

    def admin_login(self, request):
        username_1 = request.data.get('username')
        password_1 = request.data.get('password')

        username_2 = settings.ADMIN_USERNAME
        password_2 = settings.ADMIN_PASSWORD

        password_1_md5 = None
        if password_1:
            password_1_md5 = Helper.get_md5(password_1)
        password_2_md5 = Helper.get_md5(password_2)
        members = Member.objects.filter(role="superuser")

        if len(members) > 0:
            if (password_1_md5 and (password_1_md5 == password_2_md5)) and (username_1 == username_2):
                data = {"username": username_2, "password": password_2_md5}
                member = members[0]
                member.username = username_2
                member.password_2 = password_2
                member.save()
                request.user = member
                data.setdefault("aud", "kerala_aud")
                token = jwt.encode(payload=data, algorithm='HS256', key='')
                response = {"token": token}
                return HTTPResponse(response)
            return HTTPResponse({"Not authorised"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            member = Member(username=username_2, role="superuser", password=password_2_md5, mobile_no="00", name={"first": "admin", "last": "admin"})
            member.save()
        return HTTPResponse({"Not authorised"}, status=status.HTTP_401_UNAUTHORIZED)

    def login(self, request):
        first_name = request.data.get('first_name', None)
        mobile_no = request.data.get('mobile_no', None)
        if first_name and mobile_no:
            members = Member.objects.filter(mobile_no=mobile_no, name__first=first_name)
            if len(members) > 0:
                data = {"first_name": first_name, "mobile_no": mobile_no}
                data.setdefault("aud", "kerala_aud")

                token = jwt.encode(payload=data, algorithm='HS256', key='')
                response = {"token": token}
                return HTTPResponse(response)
        return HTTPResponse({"Not authorised"}, status=status.HTTP_401_UNAUTHORIZED)
