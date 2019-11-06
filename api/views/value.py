
from api import models
from api.auth.auth import Auth
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response


"""阈值序列化类
"""

class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Value
        fields = "__all__"
"""
阈值操作
"""
class ValueView(APIView):
    authentication_classes = [Auth,]
    def get(self, request, *args, **kwargs):
        ret = {'code':1000,'data':None}
        device_id = request.query_params.get('device_id')
        print(request.query_params)
        try:
            if device_id == '':
                ret['code'] = 1002
                ret['error'] = '请选择设备'
            else:
                values = models.DeviceInfo.objects.filter(device_id=device_id).first()
                # obj = values.value_set.all()
                obj = models.Value.objects.filter(device_id=values)
                if obj.exists():
                    ser = ValueSerializer(instance=obj, many=True)
                    ret['data'] = ser.data
                    print(ser.data)
                else:
                    ret['code'] = 1003,
                    ret['error'] = '该设备未设置阈值'

        except Exception as e:
            print(e)
            ret['code'] = 1001
            ret['error'] = '获取阈值失败'
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
                password = request.data.get('password')

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
