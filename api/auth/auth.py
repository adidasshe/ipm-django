from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from api import models

"""
用户认证,如果没有带有正确的token就不允许访问该API
"""


class Auth(BaseAuthentication):
    def authenticate(self, request):
        # print('loding...')
        token = request.query_params.get('token')
        # if token != None:
        #     obj = models.UserToken.objects.filter(token=token).first()
        # else:
        #     # 从前端请求头中拿到用户tokenaaaaaaaaaaaaa
        #     token = request.META.get('HTTP_TOKEN', None)
        obj = models.UserToken.objects.filter(token=token).first()
        if not obj:
            raise AuthenticationFailed({'code': 1001, 'error': '认证失败'})
        return (obj.user.username, obj)
