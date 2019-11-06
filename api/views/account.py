from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from api import models
import uuid
from django.contrib.auth.hashers import make_password, check_password

class TokenSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='username.username')
    class Meta:
        model = models.UserToken
        # fields = "__all__"
        fields = ['user','token','username']

"""
用户登录认证
"""
class AuthView(APIView):
    def post(self,request,*args,**kwargs):
        print(request.data)
        ret = {'code':1000}
        # 获取前端传来的用户名密码
        user  =request.data.get('username')
        pwd  =request.data.get('password')
        # user  =request.data.get('user')
        # pwd  =request.data.get('pwd')
        print(user,pwd)
        password = make_password(pwd,'447609mp')
        print(password)
        obj = models.Register.objects.filter(username=user, password=password).first()
        print("======>")
        if obj:
            try:
                # 生成UUID
                uid = str(uuid.uuid4())
                print(uid)
                # 如果用户token不存在就创建，存在就更新
                models.UserToken.objects.update_or_create(user=obj, defaults={'token': uid})
                ret['token'] = uid
                ret['name'] = user
            except Exception as e:
                print(e)
                ret['code'] = 1002
                ret['error'] = '登录错误...请稍后再试'

        else:
            ret['code'] = 1001
            ret['error'] = '用户名或密码错误'
            print('<<<<<')
        return Response(ret)
