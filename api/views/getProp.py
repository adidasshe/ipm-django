from django.shortcuts import render, HttpResponse
import json
from api import models
from api.auth.auth import Auth
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response

"""用户序列化类
"""


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.CharField(source='get_prop_display')

    class Meta:
        model = models.Register
        fields = ['roles', 'username']


"""
用户操作
"""


class GetProp(APIView):
    authentication_classes = [Auth, ]

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'data': None}
        # print(request.data)
        try:
            token = request.query_params.get('token')
            print(token)
            user = models.UserToken.objects.filter(token=token).first().user.username
            print(user)
            obj = models.Register.objects.filter(username=user).first()
            ser = UserSerializer(instance=obj, many=False)
            roles = ser.data.get('roles').split(',')
            name = ser.data.get('username')
            data ={'roles':None,'name':None}
            data['roles'] = roles
            data['name'] = name
            ret['data'] = data
            # print(data)
        except Exception as e:
            print(e)
            ret['code'] = 1001
            ret['error'] = '获取用户权限失败'
        return Response(ret)
