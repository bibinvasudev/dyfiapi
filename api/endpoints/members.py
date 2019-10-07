from datetime import datetime
import csv
from collections import OrderedDict
from django.http import HttpResponse

from members.models import Member
from levels.models import Level
from groups.models import Group
from core.endpoint import Endpoint
from core.response import HTTPResponse
from members.models import Name


class MemberEndpoint(Endpoint):

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        user = request.user
        level = Level.safe_get(data.get('level_id'))
        groups = Group.objects.filter(id__in=data.get('group_ids'))
        member = Member()
        name = Name(first=data.get('first_name', ""), middle=data.get('middle_name', ""), last=data.get('last_name', ""))
        member.name = name
        member.dob = data.get("dob", None)
        member.mobile_no = data.get("mobile_no", None)
        member.gender = data.get("gender", "male")
        member.level_id = level.to_dbref() if level else None
        member.group_ids = groups
        member.created_at = datetime.utcnow()
        member.created_by = user.to_dbref() if user.id else None
        member.save()
        response = {"id": str(member.id), "name": member.get_full_name()}
        return HTTPResponse(response)

    def update(self, request, member_id=None):
        data = request.data
        member = Member.safe_get(member_id)
        user = request.user
        if not member:
            return HTTPResponse({"No such member found !"})
        level = Level.safe_get(data.get('level_id'))
        groups = Group.objects.filter(id__in=data.get('group_ids'))
        if data.get('first_name', False):
            member.name.first = data.get('first_name')
        if data.get('middle_name', False):
            member.name.middle = data.get('middle_name')
        if data.get('last_name', False):
            member.name.last = data.get('last_name')
        member.mobile_no = data.get('mobile_no', member.mobile_no)
        member.dob = data.get('dob', member.dob)
        if level:
            member.level_id = level.to_dbref()
        if groups:
            member.group_ids = groups
        member.updated_at = datetime.utcnow()
        member.updated_by = user.to_dbref() if user.id else None
        member.save()
        return self.retrieve(request, member_id=member_id)

    def list(self, request, *args, **kwargs):
        group = Group.safe_get(request.query_params.get('group_id', None))
        if group:
            members = Member.objects.filter(group_id=group.id)
        else:
            members = Member.objects.all()
        response = []
        for member in members:
            response.append({"id": str(member.id), "name": member.get_full_name()})
        return HTTPResponse(response)

    def retrieve(self, request, member_id=None):
        member = Member.safe_get(member_id)
        if not member:
            return HTTPResponse({"No such member found !"})
        response = {
            "id": str(member.id),
            "name": member.get_full_name(),
            "mobile_no": member.mobile_no,
            "dob": datetime.strftime(member.dob, "%d/%m/%Y"),
            "level_id": str(member.level_id.id) if member.level_id else "",
            "level_no": member.level_id.level_no if member.level_id else "",
            "level_title": member.level_id.title if member.level_id else "",
            "group_id": str(member.group_id.id) if member.group_id else "",
            "group_title": member.group_id.title if member.group_id else ""
        }
        return HTTPResponse(response)

    def delete(self, request, member_id=None):
        member = Member.safe_get(member_id)
        if not member:
            return HTTPResponse({"No such member found !"})
        member.delete()
        response = {
        }
        return HTTPResponse(response)

    def get_my_profile(self, request):
        user = request.user
        if user.id:
            return self.retrieve(request, member_id=str(user.id))
        else:
            return HTTPResponse({"No such member found!"})

    def update_my_profile(self, request):
        user = request.user
        if user.id:
            return self.update(request, member_id=str(user.id))
        else:
            return HTTPResponse({"No such member found!"})


def get_members_details(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=MembersDetails.csv"
    attributes = OrderedDict([('name.first', 'First Name'),
                              ('name.last', 'Last Name'),
                              ('age', 'Age'),
                              ('gender', 'Gender'),
                              ('mobile_no', 'Mobile No')])

    csv_writer = csv.writer(response, csv.excel)
    csv_writer.writerow([label for _, label in attributes.items()])
    for member in Member.objects.all():
        values = []
        for attr, _ in attributes.items():
            values.append(eval('member.' + attr))
        csv_writer.writerow(values)
    return response



