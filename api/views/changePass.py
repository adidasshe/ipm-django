from django.shortcuts import render,HttpResponse

from api import models
from api.auth.auth import Auth


from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password

"""
用户序列化类
"""

class UserSerializer(serializers.ModelSerializer):
    #取模型类定义的choices字段
    sex = serializers.CharField(source='get_sex_display')
    prop = serializers.CharField(source='get_prop_display')
    class Meta:
        model = models.Register
        fields = "__all__"
"""
修改密码
"""
class ChangePass(APIView):
    authentication_classes = [Auth,]

    def put(self, request, *args, **kwargs):
        print("dasda", request.data)
        ret = {'code': 1000, 'data': None}
        try:
            username = request.data.get('username')
            pwd = request.data.get('oldPass')
            password = make_password(pwd, '447609mp')
            print(username)
            obj = models.Register.objects.filter(username = username,password=password)
            if not obj:
                ret['code'] = 1002
                ret['error'] = '请输入正确的原密码！'
            else:
                newpass = request.data.get('checkPass')
                password = make_password(newpass,'447609mp')

                models.Register.objects.filter(username = username).update(password = password
                                                                  )
        except Exception as e:
            print(e)
            ret['code'] = 1001
            ret['error'] = '修改密码失败！'

        return Response(ret)
