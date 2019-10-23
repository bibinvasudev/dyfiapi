from datetime import datetime
import csv
from collections import OrderedDict
from django.http import HttpResponse
from rest_framework_mongoengine import viewsets
from mongoengine import Q
from members.models import Member
from levels.models import Level
from groups.models import Group
from core.endpoint import Endpoint
from core.response import HTTPResponse
from core.pagination import MediumSizePagination
from members.models import Name
from api.serializers.member_serializers import MemberSerializer


class MembersViewSet(viewsets.ModelViewSet):
    model = Group
    serializer_class = MemberSerializer
    pagination_class = MediumSizePagination


class MemberEndpoint(Endpoint):

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        user = request.user
        level = Level.safe_get(data.get('level_id'))
        groups = Group.objects.filter(id__in=data.get('group_ids', []))
        member = Member()
        name = Name(first=data.get('first_name', None), middle=data.get('middle_name', ""), last=data.get('last_name', None))
        member.name = name
        dob = data.get('dob', None)
        if dob:
            member.dob = datetime.strptime(dob, "%d/%m/%Y")
        member.mobile_no = data.get("mobile_no", None)
        member.address = data.get("address", "")
        member.job = data.get("job", "")
        member.email = data.get("email", "")
        member.qualification = data.get("qualification", "")
        member.blood_group = data.get("blood_group", "")
        member.age = data.get("age", 0)
        member.is_member_already = data.get("is_member_already", False)
        member.gender = data.get("gender", "male")

        if request.data.get("image", None):
            member.image.put(request.data.get("image"), encoding='utf-8')

        if level:
            member.level_id = level.to_dbref()
        if len(groups) > 0:
            member.group_ids = groups
        elif request.user and request.user.group_ids and request.user.higher_group:
            member.group_ids = [request.user.higher_group]
            member.level_id = request.user.higher_group.level_id
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
        groups = Group.objects.filter(id__in=data.get('group_ids', []))
        if data.get('first_name', False):
            member.name.first = data.get('first_name')
        if data.get('middle_name', False):
            member.name.middle = data.get('middle_name')
        if data.get('last_name', False):
            member.name.last = data.get('last_name')

        if request.data.get("image", None):
            member.image.replace(request.data.get("image"), encoding='utf-8')

        member.mobile_no = data.get('mobile_no', member.mobile_no)
        member.address = data.get("address", member.address)
        member.job = data.get("job", member.job)
        member.email = data.get("email", member.email)
        member.qualification = data.get("qualification", member.qualification)
        member.blood_group = data.get("blood_group", member.blood_group)
        member.age = data.get("age", member.age)
        member.is_member_already = data.get("is_member_already", member.is_member_already)
        member.gender = data.get("gender", member.gender)

        dob = data.get('dob', None)
        if dob:
            member.dob = datetime.strptime(dob, "%d/%m/%Y")
        if level:
            member.level_id = level.to_dbref()
        if len(groups) > 0:
            higher_group = sorted(groups, key=lambda g: g.level_id.level_no)[-1]
            member.group_ids = groups
            for group in groups:
                group.add_member(member)
            member.is_active = True
            member.level_id = higher_group.level_id
        member.updated_at = datetime.utcnow()
        member.updated_by = user.to_dbref() if user.id else None
        member.save()
        return self.retrieve(request, member_id=member_id)

    def list(self, request, *args, **kwargs):
        query = Q()
        for qp in request.query_params:
            if qp == "first_name":
                query |= Q(name__first=request.query_params.get(qp))
            elif qp == "middle_name":
                query |= Q(name__middle=request.query_params.get(qp))
            elif qp == "last_name":
                query |= Q(name__last=request.query_params.get(qp))
            elif qp == "group_id":
                group = Group.safe_get(request.query_params.get(qp))
                if group:
                    query |= Q(group_ids__in=[group.id])
            else:
                query |= Q(**{qp: request.query_params.get(qp)})

        members = Member.objects.filter(query)
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
            "address": member.address,
            "job": member.job,
            "age": member.age,
            "gender": member.gender,
            "email": member.email,
            "qualification": member.qualification,
            "is_member_already": member.is_member_already,
            "blood_group": member.blood_group,
            "dob": datetime.strftime(member.dob, "%d/%m/%Y"),
            "level_id": str(member.level_id.id) if member.level_id else "",
            "level_no": member.level_id.level_no if member.level_id else "",
            "level_title": member.level_id.title if member.level_id else "",
            "group_id": str(member.group_id.id) if member.group_id else "",
            "group_title": member.group_id.title if member.group_id else "",
            "image": member.image.read() if member.image else ""
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

    def update_my_profile_image(self, request):
        user = request.user
        if request.data.get("image", None):
            if user and user.image:
                user.image.replace(request.data.get("image"), encoding='utf-8')
            else:
                user.image.put(request.data.get("image"), encoding='utf-8')
            user.save()
        return self.get_my_profile_image(request)

    def get_my_profile_image(self, request):
        user = request.user
        if user and not user.image:
            return HTTPResponse({"Please upload the image!"})
        return HTTPResponse({"data": user.image.read()})


class ExportDataEndpoint(Endpoint):

    def get_members_details(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=MembersDetails.csv"
        attributes = OrderedDict([('name.first', 'First Name'),
                                  ('name.last', 'Last Name'),
                                  ('age', 'Age'),
                                  ('gender', 'Gender'),
                                  ('mobile_no', 'Mobile No')])

        csv_writer = csv.writer(response, csv.excel)
        csv_writer.writerow([label for _, label in attributes.items()])
        group = Group.safe_get(request.query_params.get('group_id', None))
        if group:
            members = Member.objects.filter(group_ids__in=[group.id])
        else:
            members = Member.objects.all()
        for member in members:
            values = []
            for attr, _ in attributes.items():
                values.append(eval('member.' + attr))
            csv_writer.writerow(values)
        return response



