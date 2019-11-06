from django.middleware.common import CommonMiddleware

class MiddlewareMixin:
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        response = response or self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response
"""
利用中间件加响应头，解决跨域简单请求
"""
class CORSMiddleware(MiddlewareMixin):
    def process_response(self,request,response):
        #添加响应头
        #允许其它域名来请求数据
        response['Access-Control-Allow-Origin'] = "*"
        #允许携带Content-Type请求头
        # response['Access-Control-Allow-Headers'] = "Content-Type,Host"
        # response['Access-Control-Allow-Methods'] = "DELETE,PUT"

        if request.method == "OPTIONS":
            response['Access-Control-Allow-Headers'] = "Content-Type,Host,token"
            response['Access-Control-Allow-Methods'] = "GET,DELETE,PUT,POST"

        return response
