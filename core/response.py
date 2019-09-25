from rest_framework.response import Response
import json


class HTTPResponse(Response):
    """
    Custom response structure for api call responses.
    """
    def __init__(self, data=None, status=None, template_name=None, headers=None, exception=False, content_type=None):
        if isinstance(data, str):
            self.data = json.loads(data)
        else:
            self.data = data

        super(HTTPResponse, self).__init__(data=self.data, status=status)