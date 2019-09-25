import logging
from pythonjsonlogger import jsonlogger
from rest_framework import viewsets


class Endpoint(viewsets.GenericViewSet):
    """
    All endpoints extends to this class for common functionality like
    setting up logger for error logging, and criteria object for refining query results.
    """
    logger = logging.getLogger('api')
    comparative_operators = ['gt', 'lt', 'gte', 'lte', 'icontains']

    def initial(self, request, *args, **kwargs):
        # get payload and validate
        super(Endpoint, self).initial(request, args, kwargs)
        # Write here to use `constructor`
        handler = logging.StreamHandler()
        handler.setFormatter(jsonlogger.JsonFormatter())
        self.logger.addHandler(handler)
        pass

    def get_logger(self):
        return self.logger

