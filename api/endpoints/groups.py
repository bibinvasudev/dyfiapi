from datetime import datetime

from groups.models import Group
from levels.models import Level
from members.models import Member
from core.endpoint import Endpoint
from core.response import HTTPResponse


class GroupEndpoint(Endpoint):

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        user = request.user
        level = Level.safe_get(data.get('level_id'))
        admin = Member.safe_get(data.get('admin_id'))
        parent_group = Group.safe_get(data.get('parent_group_id'))
        group = Group()
        group.title = data.get('title', '')
        group.level_id = level.to_dbref() if level else None
        group.admin_id = admin.to_dbref() if admin else None
        group.created_at = datetime.utcnow()
        group.created_by = user.to_dbref() if user.id else None
        group.parent_group_id = parent_group.id if parent_group else None
        group.save()
        response = {"id": str(group.id), "title": group.title}
        return HTTPResponse(response)

    def update(self, request, group_id=None):
        data = request.data
        group = Group.safe_get(group_id)
        user = request.user
        if not group:
            return HTTPResponse({"No such group found !"})
        level = Level.safe_get(data.get('level_id'))
        admin = Member.safe_get(data.get('admin_id'))
        parent_group = Group.safe_get(data.get('parent_group_id'))
        group.title = data.get('title', group.title)
        if level:
            group.level_id = level.to_dbref()
        if admin:
            group.admin_id = admin.to_dbref()
        if parent_group:
            group.parent_group_id = parent_group.to_dbref()
        group.updated_at = datetime.utcnow()
        group.updated_by = user.to_dbref() if user.id else None
        group.save()
        response = {"id": str(group.id), "title": group.title}
        return HTTPResponse(response)

    def list(self, request, *args, **kwargs):
        groups = Group.objects.all()
        response = []
        try:
            for group in groups:
               response.append({"id": str(group.id), "title": group.title, "level_title": group.level_id.title})
        except:
            pass
        return HTTPResponse(response)

    def retrieve(self, request, group_id=None):
        group = Group.safe_get(group_id)
        if not group:
            return HTTPResponse({"No such group found !"})
        response = {
            "id": str(group.id),
            "title": group.title,
            "level_id": str(group.level_id.id) if group.level_id else "",
            "level_no": group.level_id.level_no,
            "level_title": group.level_id.title,
            "admin_id": str(group.admin_id.id) if group.admin_id else "",
            "admin_name": group.admin_id.get_full_name() if group.admin_id else '',
            "parent_group_id": str(group.parent_group_id.id) if group.parent_group_id else "",
            "parent_group_name": group.parent_group_id.title if group.parent_group_id else ""
        }
        return HTTPResponse(response)

    def delete(self, request, group_id=None):
        group = Group.safe_get(group_id)
        if not group:
            return HTTPResponse({"No such group found !"})
        group.delete()
        response = {
        }
        return HTTPResponse(response)
