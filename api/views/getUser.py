from django.shortcuts import render,HttpResponse

from api import models
from api.auth.auth import Auth


from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response


"""用户序列化类
"""

class UserSerializer(serializers.ModelSerializer):
    #取模型类定义的choices字段
    sex = serializers.CharField(source='get_sex_display')
    prop = serializers.CharField(source='get_prop_display')
    class Meta:
        model = models.Register
        fields = "__all__"
"""
用户搜索
"""
class GetUserView(APIView):
    authentication_classes = [Auth,]
    def get(self, request, *args, **kwargs):
        ret = {'code':1000,'data':None}
        # print(request.query_params.get('name'))
        name = request.query_params.get('name')
        try:
            obj = models.Register.objects.filter(username__contains=name)
            ser = UserSerializer(instance=obj, many=True)
            ret['data'] = ser.data
        except Exception as e:
            print(e)
            ret['code'] =1001
            ret['error'] = '获取用户列表失败'
        return Response(ret)



