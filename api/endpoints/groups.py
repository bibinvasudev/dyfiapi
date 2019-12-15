from datetime import datetime

from groups.models import Group
from levels.models import Level
from members.models import Member
from core.endpoint import Endpoint
from core.response import HTTPResponse
from api.serializers.group_serializers import GroupSerializer


class GroupEndpoint(Endpoint):

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        user = request.user
        if not (user.is_admin or user.is_superuser):
            return HTTPResponse({"Error": "Cannot create a Group !! Only admin can create a new group!!"})
        level = Level.safe_get(data.get('level_id'))
        admins = Member.objects.filter(id__in=data.get('admin_ids', []))
        parent_group = Group.safe_get(data.get('parent_group_id'))
        group = Group()
        group.title = data.get('title', '')
        group.admin_ids = [request.user.to_dbref()]
        if level:
            group.level_id = level.to_dbref()
        elif request.user and request.user.level_id:
            sub_levels = Level.objects.filter(level_no=request.user.level_id.level_no - 1)
            if len(sub_levels) > 0:
                group.level_id = sub_levels[0]
            else:
                return HTTPResponse({"Error": "Cannot create Group !! You are at the lowest level!!"})
        if parent_group:
            group.parent_group_id = parent_group.to_dbref()
        elif request.user.group_ids and request.user.higher_group:
            group.parent_group_id = request.user.higher_group
        if len(admins) > 0:
            for admin in admins:
                if admin.is_admin:
                    return HTTPResponse({"Error": admin.name.first + " is already an admin of a group !!"})
                admin.is_admin = True
                admin.save()
                group.admin_ids.append(admin.to_dbref)
        if request.data.get("image", None):
            group.image.put(request.data.get("image"), encoding='utf-8')
        group.created_at = datetime.utcnow()
        group.created_by = user.to_dbref() if user.id else None
        group.save()
        if request.user and hasattr(request.user, "id"):
            group.add_member(members=[request.user])
            group.add_member(members=admins)
        response = GroupSerializer(group, context={"request": request}).data
        return HTTPResponse(response)

    def update(self, request, group_id=None):
        data = request.data
        group = Group.safe_get(group_id)
        user = request.user
        if not group:
            return HTTPResponse({"No such group found !"})
        level = Level.safe_get(data.get('level_id'))
        admins = Member.objects.filter(id__in=data.get('admin_ids', []))
        members = Member.objects.filter(id__in=data.get('member_ids', []))
        parent_group = Group.safe_get(data.get('parent_group_id'))
        group.title = data.get('title', group.title)
        if level:
            group.level_id = level.to_dbref()
        if len(admins) > 0:
            for admin in admins:
                # if admin.is_admin:
                #     return HTTPResponse({"Error": admin.name.first + " is already an admin of a group !!"})
                admin.is_admin = True
                admin.save()
                group.modify(add_to_set__admin_ids=admin.id)
        if parent_group:
            group.parent_group_id = parent_group.to_dbref()
        if request.data.get("image", None):
            group.image.replace(request.data.get("image"), encoding='utf-8')
        group.updated_at = datetime.utcnow()
        group.updated_by = user.to_dbref() if user.id else None
        group.save()
        if len(members) > 0:
            group.add_member(members=members)
            group.add_member(members=admins)
        response = GroupSerializer(group, context={"request": request}).data
        return HTTPResponse(response)

    def list(self, request, *args, **kwargs):
        groups = []
        if request.user and request.user.is_admin:
            groups = Group.objects.filter(created_by=request.user.id)
        if request.user and request.user.is_superuser:
            groups = Group.objects.all()
        response = GroupSerializer(groups, many=True, context={"request": request}).data
        return HTTPResponse(response)

    def get_my_groups(self, request, *args, **kwargs):
        response = []
        groups = []
        if request.user and (len(request.user.group_ids) > 0):
            groups = request.user.group_ids
        for group in groups:
            group_data = {"id": str(group.id),
                          "title": group.title,
                          "level_title": group.level_id.title,
                          "members_count": len(group.member_ids),
                          "hierarchy": group.get_hierarchy()}
            response.append(group_data)
        return HTTPResponse(response)

    def retrieve(self, request, group_id=None):
        group = Group.safe_get(group_id)
        if not group:
            return HTTPResponse({"No such group found !"})
        response = GroupSerializer(group, context={"request": request}).data
        return HTTPResponse(response)

    def delete(self, request, group_id=None):
        group = Group.safe_get(group_id)
        if not group:
            return HTTPResponse({"No such group found !"})
        group.delete()
        response = {
        }
        return HTTPResponse(response)

    def add_admin(self, request, group_id=None):
        group = Group.safe_get(group_id)
        if not group:
            return HTTPResponse({"No such group found !"})

        member = Member.safe_get(request.data.get("member_id"))
        if not member:
            return HTTPResponse({"No such member found !"})

        group.modify(add_to_set__admin_ids=member.id)
        member.is_admin = True
        member.save()
        response = GroupSerializer(group, context={"request": request}).data
        return HTTPResponse(response)

    def remove_admin(self, request, group_id=None):
        group = Group.safe_get(group_id)
        if not group:
            return HTTPResponse({"No such group found !"})

        member = Member.safe_get(request.data.get("member_id"))
        if not member:
            return HTTPResponse({"No such member found !"})

        group.modify(pull__admin_ids=member.id)
        response = GroupSerializer(group, context={"request": request}).data
        return HTTPResponse(response)
