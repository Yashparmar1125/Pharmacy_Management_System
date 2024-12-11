import logging
from django.http import Http404, HttpResponseNotFound, HttpResponseServerError, HttpResponseForbidden
from django.template import loader
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        logger.error(f"Exception occurred: {exception}", exc_info=True)

        if isinstance(exception, Http404):
            template = loader.get_template('Error/404.html')
            return HttpResponseNotFound(template.render())
        elif isinstance(exception, PermissionDenied):
            template = loader.get_template('Error/403.html')
            return HttpResponseForbidden(template.render())
        else:  # Catch all other exceptions
            template = loader.get_template('Error/500.html')
            return HttpResponseServerError(template.render())
