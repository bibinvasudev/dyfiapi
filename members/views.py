from mongoengine import Q
from django.shortcuts import render
from django.views.generic.edit import FormView
from .models import Member
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import MemberForm, MemberSearchForm
from django.views.generic.base import TemplateView
from groups.models import Group
from levels.models import Level
from members.models import Address
from members.models import Name
from api.serializers.member_serializers import MemberSimpleSerializer


class MembersListView(FormView):

    def get(self, request):
        if not request.session.get('is_authenticated'):
            return HttpResponseRedirect(reverse('web:login'))
        data = {"members": Member.objects.all()}
        return render(request, 'members/members_list.html', data)


class MemberView(TemplateView):
    form_class = MemberForm
    template_name = 'members/add_member.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        districts = []
        district_level = Level.objects.filter(level_no=4)
        if len(district_level):
            district_level = district_level[0]
            districts = Group.objects.filter(level_id=district_level.id).values_list('id', 'title')
        data = {
            'districts': districts,
            'members': MemberSimpleSerializer(Member.objects.all(), many=True, context={"request": request}).data
        }
        return render(request, self.template_name, {'form': form, 'data': data})

    def post(self, request, *args, **kwargs):
        member_form = self.form_class(request.POST)
        if member_form.is_valid():
            data = member_form.cleaned_data
            image_data = data.pop('image', "")
            house = data.pop('house', "")
            street = data.pop('street', "")
            city = data.pop('city', "")
            district = data.pop('district', "")
            state = data.pop('state', "")
            pin = data.pop('pin_code', "")
            first_name = data.pop('first_name', "")
            last_name = data.pop('last_name', "")
            group_ids = data.pop('group_ids', [])
            member = Member(**data)
            member.name = Name(first=first_name, last=last_name)
            member.group_ids = [group.to_dbref() for group in Group.objects.filter(id__in=group_ids)]
            member.address = Address(house=house, street=street, city=city, district=district, state=state, pin_code=pin)
            member.image.put(image_data, encoding='utf-8')
            member.save()
        return HttpResponseRedirect(reverse('web:members:add_member'))

    @staticmethod
    def load_groups(request):
        group = Group.safe_get(request.GET.get('group_id'))
        groups = []
        if group:
            groups = Group.objects.filter(parent_group_id=group.id).values_list('id', 'title')
        return render(request, 'members/group_dropdown.html', {'groups': groups})


class MemberSearchView(TemplateView):
    form_class = MemberSearchForm
    template_name = 'members/search_member.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        data = {
            'members': MemberSimpleSerializer(Member.objects.all(), many=True, context={"request": request}).data
        }
        return render(request, self.template_name, {'form': form, 'data': data})

    def post(self, request, *args, **kwargs):
        search_form = self.form_class(request.POST)
        data = {}
        if search_form.is_valid():
            data = search_form.cleaned_data
        query = Q()
        for qp in data:
            if data.get(qp):
                if qp == "first_name":
                    query &= Q(name__first=data.get(qp))
                elif qp == "last_name":
                    query &= Q(name__last=data.get(qp))
                elif qp == "group_id":
                    group = Group.safe_get(data.get(qp))
                    if group:
                        query &= Q(group_ids__in=[group.id])
                else:
                    query &= Q(**{qp: data.get(qp)})

        members = Member.objects.filter(query)
        data = {
            'members': MemberSimpleSerializer(members, many=True, context={"request": request}).data
        }
        return render(request, self.template_name, {'form': search_form, 'data': data})

