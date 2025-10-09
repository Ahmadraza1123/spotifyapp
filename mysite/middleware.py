from django.utils.deprecation import MiddlewareMixin

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("Request aayi!")

    def process_response(self, request, response):
        print("Response ja raha hai!")
        return response
