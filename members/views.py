from django.shortcuts import render
from django.views.generic.edit import FormView
from .models import Member
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import MemberForm, MemberSearchForm
from django.views.generic.base import TemplateView
from groups.models import Group
from levels.models import Level


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
        # mekhalas = []
        # blocks = []
        # units = []
        district_level = Level.objects.filter(level_no=4)
        if len(district_level):
            district_level = district_level[0]
            districts = Group.objects.filter(level_id=district_level.id).values_list('id', 'title')
        # mekhala_level = Level.objects.filter(level_no=3)
        # if len(mekhala_level):
        #     mekhala_level = mekhala_level[0]
        #     mekhalas = Group.objects.filter(level_id=mekhala_level.id).values_list('id', 'title')
        # block_level = Level.objects.filter(level_no=2)
        # if len(block_level):
        #     block_level = block_level[0]
        #     blocks = Group.objects.filter(level_id=block_level.id).values_list('id', 'title')
        # unit_level = Level.objects.filter(level_no=1)
        # if len(unit_level):
        #     unit_level = unit_level[0]
        #     units = Group.objects.filter(level_id=unit_level.id).values_list('id', 'title')
        data = {
            'districts': districts
        }
        return render(request, self.template_name, {'form': form, 'data': data})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        messages = []
        import pdb
        pdb.set_trace()

        if form.is_valid():
            opportunity_id = form.cleaned_data['opportunity_id']
            associate_id = form.cleaned_data['associate_id']
            messages.append(opportunity_id + ' ' + associate_id)

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
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        messages = []

        if form.is_valid():
            opportunity_id = form.cleaned_data['opportunity_id']
            associate_id = form.cleaned_data['associate_id']
            messages.append(opportunity_id + ' ' + associate_id)

        return render(request, self.template_name, {'form': form, 'messages': messages})

