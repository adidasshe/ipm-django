
from api import models
from api.auth.auth import Auth
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password

"""用户序列化类
"""
# class UserSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     user_name = serializers.CharField()
#     user_prop = serializers.CharField()
#     user_pass = serializers.CharField()
#     name = serializers.CharField()
#     sex = serializers.CharField()
#     age = serializers.CharField()
#     company = serializers.CharField()
#     duty = serializers.CharField()
#     phone = serializers.CharField()
#     desc = serializers.CharField()
class UserSerializer(serializers.ModelSerializer):
    #取模型类定义的choices字段
    sex = serializers.CharField(source='get_sex_display')
    prop = serializers.CharField(source='get_prop_display')
    class Meta:
        model = models.Register
        fields = "__all__"
"""
用户操作
"""
class UserView(APIView):
    authentication_classes = [Auth,]
    def get(self, request, *args, **kwargs):
        ret = {'code':1000,'data':None}
        print(request.query_params)
        try:
            obj = models.Register.objects.all()
            ser = UserSerializer(instance=obj, many=True)
            ret['data'] = ser.data
        except Exception as e:
            print(e)
            ret['code'] =1001
            ret['error'] = '获取用户列表失败'
        return Response(ret)

    def post(self, request, *args, **kwargs):
        print("dasda",request.data)
        ret = {'code': 1000, 'data': None}
        try:

            username = request.data.get('username')
            obj = models.Register.objects.filter(username=username).first()
            if obj:
                ret['code'] = 1002
                ret['error'] = '用户已存在'
            else:
                pwd = request.data.get('password')
                password = make_password(pwd, '447609mp')
                age = request.data.get('age')
                company = request.data.get('company')
                desc = request.data.get('desc')
                duty = request.data.get('duty')
                name = request.data.get('name')
                phone = request.data.get('phone')
                prop = request.data.get('prop')
                sex = request.data.get('sex')
                models.Register.objects.create(username=username,password= password, prop= prop,
                                                                  name= name, sex= sex,
                                                                  age= age, company= company, duty= duty,
                                                                  phone=phone,desc= desc,
                                                                  )
        except Exception as e:
            print(e)
            ret['code'] = 10
            ret['error'] = '添加失败'

        return Response(ret)

    def put(self, request, *args, **kwargs):
        print("dasda", request.data)
        ret = {'code': 1000, 'data': None}
        try:

            id = request.data.get('id')
            username = request.data.get('username')
            if id == 1:
                ret['code'] = 1002
                ret['error'] = '默认管理员用户名不能修改!'
            else:
                pwd = request.data.get('password')
                age = request.data.get('age')
                company = request.data.get('company')
                desc = request.data.get('desc')
                duty = request.data.get('duty')
                name = request.data.get('name')
                phone = request.data.get('phone')
                prop = request.data.get('prop')
                sex = request.data.get('sex')
                models.Register.objects.filter(id = id).update(prop = prop,
                                                                  name=name, sex=sex,age=age, company= company,duty=duty,
                                                                  phone=phone,desc= desc,username=username,
                                                                  )
        except Exception as e:
            print(e)
            ret['code'] = 1001
            ret['error'] = '更新失败'

        return Response(ret)

    def delete(self, request, *args, **kwargs):

        print("id", request.data)
        ret = {'code': 1000, 'data': None}
        id =None
        try:

            id = request.data.get('id')

            if id == 1:
                ret['code'] = 1002
                ret['error'] = '默认管理员不能删除'
            else:
                models.Register.objects.filter(id=id).delete()
        except Exception as e:
            ret['code'] = 1001
            ret['error'] = '删除失败'

        return Response(ret)
