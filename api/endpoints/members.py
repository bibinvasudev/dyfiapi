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
from members.models import Address
from api.serializers.member_serializers import MemberSerializer, MemberSimpleSerializer


class MembersViewSet(viewsets.ModelViewSet):
    model = Group
    serializer_class = MemberSerializer
    pagination_class = MediumSizePagination


class MemberEndpoint(Endpoint):

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        user = request.user
        if not (user.is_admin or user.is_superuser):
            return HTTPResponse({"Error": "Cannot create a Member !! Only admin can add new member!!"})
        level = Level.safe_get(data.get('level_id'))
        groups = Group.objects.filter(id__in=data.get('group_ids', []))
        member = Member()
        member.name = Name(**data.get('name', {}))
        member.address = Address(**data.get('address', {}))
        dob = data.get('dob', None)
        if dob:
            member.dob = datetime.strptime(dob, "%d/%m/%Y")
        member.mobile_no = data.get("mobile_no", None)
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
        member.created_at = datetime.utcnow()
        member.created_by = user.to_dbref() if user.id else None
        member.save()
        if len(groups) > 0:
            member.group_ids = groups
        elif request.user and request.user.group_ids and request.user.higher_group:
            higher_group = request.user.higher_group
            member.default_group = higher_group
            higher_group.add_member(members=[member], active=False)
            member.level_id = higher_group.level_id
        member.save()
        # if request.user.higher_group:
        #     request.user.higher_group.add_member(members=[member])
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
        if data.get('name', False):
            member.name = Name(**data.get('name', {}))
        if data.get('address', False):
            member.address = Address(**data.get('address', {}))
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
            for group in groups:
                group.add_member(members=[member])
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
        response = MemberSimpleSerializer(members, many=True, context={"request": request}).data
        return HTTPResponse(response)

    def retrieve(self, request, member_id=None):
        member = Member.safe_get(member_id)
        if not member:
            return HTTPResponse({"No such member found !"})
        response = MemberSerializer(member, context={"request": request}).data
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
        user = request.user
        if not (user.is_admin or user.is_superuser):
            return HTTPResponse({"Error": "You cannot export the data!! Only admin/Superuser can do it!!"})
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=MembersDetails.csv"
        attributes = OrderedDict([('name.first', 'First Name'),
                                  ('name.last', 'Last Name'),
                                  ('age', 'Age'),
                                  ('gender', 'Gender'),
                                  ('mobile_no', 'Mobile No'),
                                  ('dob', 'Date Of Birth'),
                                  ('address', 'Address'),
                                  ('job', 'Job'),
                                  ('blood_group', 'Blood Group'),
                                  ('qualification', 'Qualification'),
                                  ('email', 'Email'),
                                  ])

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



