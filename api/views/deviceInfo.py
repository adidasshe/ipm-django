from api import models
from api.auth.auth import Auth
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response

"""
设备信息序列化类
"""


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeviceInfo
        fields = "__all__"


""""
设备信息
"""


class DeviceInfoView(APIView):
    authentication_classes = [Auth, ]

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'data': None}
        # device_name = request.query_params.get('device_name')
        print(request.query_params)
        try:
            info = models.DeviceInfo.objects.all()
            ser = InfoSerializer(instance=info, many=True)
            ret['data'] = ser.data
        except Exception as e:
            ret['code'] = 1001
            ret['error'] = '获取设备列表失败'

        return Response(ret)

    def post(self, request, *args, **kwargs):
        print("dasda", request.data)
        ret = {'code': 1000, 'data': None}
        try:
            id = request.data.get('device_id')

            obj = models.DeviceInfo.objects.filter(device_id=id).first()
            if obj:
                ret['code'] = 1002
                ret['error'] = '设备已存在'
            else:
                name = request.data.get('device_name')
                desc = request.data.get('device_desc')
                lot = request.data.get('longitude')
                lat = request.data.get('latitude')
                address = request.data.get('address')
                models.DeviceInfo.objects.create(device_id=id,
                                                 device_name=name,
                                                 device_desc=desc,
                                                 longitude=lot,
                                                 latitude=lat,
                                                 address=address,
                                                 )
        except Exception as e:
            ret['code'] = 1001
            ret['error'] = '添加失败'

        return Response(ret)

    def put(self, request, *args, **kwargs):
        print("dasda", request.data)

        ret = {'code': 1000, 'data': None}
        try:
            id = request.data.get('id')
            device_id = request.data.get('device_id')
            name = request.data.get('device_name')
            desc = request.data.get('device_desc')
            lot = request.data.get('longitude')
            lat = request.data.get('latitude')
            address = request.data.get('address')
            models.DeviceInfo.objects.filter(id=id).update(device_id=device_id, device_name=name, device_desc=desc,
                                                           longitude=lot, latitude=lat, address=address,
                                                           )
        except Exception as e:
            print(e)
            ret['code'] = 1001
            ret['error'] = '更新失败'

        return Response(ret)

    def delete(self, request, *args, **kwargs):

        ret = {'code': 1000, 'data': None}
        try:
            id = request.data.get('id')
            print(id)
            models.DeviceInfo.objects.filter(id=id).delete()
        except Exception as e:
            print(e)
            ret['code'] = 1001
            ret['error'] = '删除失败'
        return Response(ret)
