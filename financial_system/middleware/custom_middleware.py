import logging
from django.http import JsonResponse
from rest_framework import status



logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logger


    def __call__(self, request):
        print("GOT HERE")
        self.logger.info(f"Request Path: {request.path}, Method: {request.method}, User: {request.user or 'AnonymousUser'}")
        response = self.get_response(request)
        return response
    


class GlobalErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
    
    def process_exception(self, reqeust, exception):
        error_response = {
            'error': 'An unexpected error occured',
            'message': str(exception),
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR
        }
        
        logger.error(f"Unhandled Exception: {str(exception)}", exc_info=True)
        
        return JsonResponse(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
