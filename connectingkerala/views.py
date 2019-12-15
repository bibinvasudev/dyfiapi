import datetime
from django.conf import settings
from members.models import Member
from core.helpers import Helper
import jwt
from core.response import HTTPResponse
from rest_framework import viewsets
from rest_framework import status
from api.serializers.member_serializers import MemberSerializer
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from .forms import LoginForm
from core.auth.authenticate import has_valid_token


def base_redirect(request):
    return HttpResponseRedirect(reverse('web:login'))


def home(request):
    return render(request, "connectingkerala/dashboard.html")


class LoginViewSet(viewsets.GenericViewSet):

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
            dob = datetime.datetime.strptime("01/01/1990", "%d/%m/%Y")
            member = Member(username=username_2, role="superuser", password=password_2_md5, dob=dob, mobile_no="00", name={"first": "admin", "last": "admin"})
            member.save()
        return HTTPResponse({"Not authorised"}, status=status.HTTP_401_UNAUTHORIZED)

    def login(self, request):
        mobile_no = request.data.get('mobile_no', None)
        dob_str = request.data.get('dob', None)
        if mobile_no and dob_str:
            dob = datetime.datetime.strptime(dob_str, "%d/%m/%Y")
            members = Member.objects.filter(dob=dob, mobile_no=mobile_no)
            if len(members) > 0:
                data = {"mobile_no": mobile_no, "dob": dob_str}
                data.setdefault("aud", "kerala_aud")

                token = jwt.encode(payload=data, algorithm='HS256', key='')
                response = {"token": token, "user_details": MemberSerializer(members[0], context={"request": request}).data}
                return HTTPResponse(response)
        return HTTPResponse({"Not authorised"}, status=status.HTTP_401_UNAUTHORIZED)


class LoginView(TemplateView):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('is_authenticated'):
            return HttpResponseRedirect('home')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        messages = []

        if form.is_valid():
            mobile_no = form.cleaned_data['mobile_no']
            dob = form.cleaned_data['dob']
            # import pdb
            # pdb.set_trace()
            # mobile_no = request.data.get('mobile_no', None)
            # dob_str = request.data.get('dob', None)
            response = {"token": False}
            if mobile_no and dob:
                dob_str = datetime.datetime.strftime(dob, "%d/%m/%Y")
                members = Member.objects.filter(dob=dob, mobile_no=mobile_no)
                if len(members) > 0:
                    data = {"mobile_no": mobile_no, "dob": dob_str}
                    data.setdefault("aud", "kerala_aud")

                    token = jwt.encode(payload=data, algorithm='HS256', key='').decode()
                    response = {"token": token}
                    if token is not None:
                        request.session['is_authenticated'] = True
                        request.session['token'] = token

                        return HttpResponseRedirect('home')
                    else:
                        messages.append('Bad login provided')

        return render(request, self.template_name, {'form': form, 'messages': messages})