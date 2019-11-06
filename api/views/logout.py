from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from api import models

class TokenSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='username.username')
    class Meta:
        model = models.UserToken
        # fields = "__all__"
        fields = ['user','token','username']

"""
用户登出
"""

class Logout(APIView):
    def post(self,request,*args,**kwargs):
        print(request.query_params)
        ret = {'code': 1000, 'data': '退出成功！'}
        try :
            token = request.query_params.get('token')
            models.UserToken.objects.filter(token=token).delete()
        except Exception as e :
            print(e)
            ret['code'] = 1001
            ret['error'] = '用户不存在'
        return Response(ret)
