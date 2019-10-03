from datetime import datetime

from levels.models import Level
from core.endpoint import Endpoint
from core.response import HTTPResponse


class LevelEndpoint(Endpoint):

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        user = request.user
        level = Level()
        level.title = data.get('title', '')
        level.level_no = data.get('level_no', 0)
        level.created_at = datetime.utcnow()
        level.created_by = user.to_dbref() if user.id else None
        level.save()
        response = {"title": level.title, "level_no": level.level_no}
        return HTTPResponse(response)

    def update(self, request, level_id=None):
        data = request.data
        user = request.user
        level = Level.safe_get(level_id)
        if not level:
            return HTTPResponse({"No such level found !"})
        level.title = data.get('title', level.title)
        level.level_no = data.get('level_no', level.level_no)
        level.updated_at = datetime.utcnow()
        level.updated_by = user.to_dbref() if user.id else None
        level.save()
        return self.retrieve(request, level_id=level_id)

    def list(self, request, *args, **kwargs):
        levels = Level.objects.all()
        response = []
        for level in levels:
            response.append({"id": str(level.id), "title": level.title, "level_no": level.level_no})
        return HTTPResponse(response)

    def retrieve(self, request, level_id=None):
        level = Level.safe_get(level_id)
        if not level:
            return HTTPResponse({"No such level found !"})
        response = {"id": str(level.id), "title": level.title, "level_no": level.level_no}
        return HTTPResponse(response)

    def delete(self, request, level_id=None):
        level = Level.safe_get(level_id)
        if not level:
            return HTTPResponse({"No such level found !"})
        level.delete()
        return HTTPResponse({})
