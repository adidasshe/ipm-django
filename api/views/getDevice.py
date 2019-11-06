
from api import models
from api.auth.auth import Auth
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response

"""设备信息序列化类
"""
class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeviceInfo
        fields = "__all__"

""""
设备搜索
"""
class GetDeviceView(APIView):
    authentication_classes = [Auth, ]

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'data': None}
        name = request.query_params.get('name')
        print(request.query_params)
        if name :
            try:
                info = models.DeviceInfo.objects.filter(device_name__contains=name)
                ser = InfoSerializer(instance=info, many=True)
                ret['data'] = ser.data
                print(ser.data)
            except Exception as e:
                ret['code'] = 1001
                ret['error'] = '获取设备列表失败'
        else:
            print("dasda", request.data)
            name = request.data.get('deviceName')
            print("name2",name)
            try:
                info = models.DeviceInfo.objects.filter(device_name__contains=name)
                ser = InfoSerializer(instance=info, many=True)
                ret['data'] = ser.data
                print(ser.data)
            except Exception as e:
                ret['code'] = 1001
                ret['error'] = '获取设备列表失败'
        return Response(ret)


