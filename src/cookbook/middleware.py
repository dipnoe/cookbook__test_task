from http import HTTPStatus
from django.core.exceptions import ObjectDoesNotExist

from django.http import JsonResponse


class ModelDoesNotExistExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    @staticmethod
    def process_exception(request, exception):
        if not isinstance(exception, ObjectDoesNotExist):
            return None
        return JsonResponse(
            {'error': str(exception)},
            status=HTTPStatus.NOT_FOUND
        )
