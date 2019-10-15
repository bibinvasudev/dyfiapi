from config.models import Config
from core.endpoint import Endpoint
from core.response import HTTPResponse


class ConfigEndpoint(Endpoint):

    def create(self, request, *args, **kwargs):
        conf = Config.objects.first()
        if not conf:
            conf = Config()
        conf.banner_image.put(request.data.get("banner_image"), encoding='utf-8')
        conf.save()
        return HTTPResponse({"Image uploaded"})

    def update(self, request, group_id=None):
        conf = Config.objects.first()
        if not conf:
            conf = Config()
        conf.banner_image.replace(request.data.get("banner_image"), encoding='utf-8')
        conf.save()
        return HTTPResponse({"Image uploaded"})

    def retrieve(self, request, level_id=None):
        conf = Config.objects().first()
        if not conf:
            return HTTPResponse({"Please upload the image!"})

        return HTTPResponse({"data": conf.banner_image.read()})
