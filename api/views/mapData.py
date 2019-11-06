import time

from api import models
from api.auth.auth import Auth
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
import json


"""设备数据序列化类
"""


class InfoSerializer(serializers.ModelSerializer):
    # device_id = serializers.CharField(source='device_id')
    # log = serializers.CharField(source='longitude')
    # lat = serializers.CharField(source='latitude')
    # name = serializers.CharField(source='device_name')
    # 设置日期格式化格式
    # date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = models.DeviceInfo
        # fields = ['device_id','name','log','lat',]
        fields = "__all__"
        # depth = 2
class DataSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(source='device_id.device_id')
    log = serializers.FloatField(source='device_id.longitude')
    lat = serializers.FloatField(source='device_id.latitude')
    name = serializers.CharField(source='device_id.device_name')
    s1 = serializers.IntegerField(source='switch1')
    s2 = serializers.IntegerField(source='switch2')
    s3 = serializers.IntegerField(source='switch3')
    # 设置日期格式化格式
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = models.DeviceData
        fields = ['device_id','name','date','s1','s2','s3','lat','log']
        # fields = "__all__"
        # depth = 2


"""
地图数据
"""


class MapDataView(APIView):
    authentication_classes = [Auth, ]

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'data': None}
        list =[]

        try:

            obj = models.DeviceInfo.objects.all()

            print(obj.count())
            for i in range(obj.count()):

                data = obj[i].devicedata_set.all().order_by('id').reverse()[:1]
                ser = DataSerializer(instance=data, many=True)
                # list.append(ser.data)
                # print(ser.data)
                list.append(ser.data)
            print(len(list))
            # for j in range(0,len(list)):
            #     print(list[j][0].get("name"))
            ret['time'] = int(time.time())
            # print(ret.get('time'))
            ret['data'] = list



            # ser = InfoSerializer(instance=obj, many=True)
            # ret['data'] = ser.data
            # print(ser.data[0].get("longitude"))


        except Exception as e:
            print(e)
            ret['code'] = 1001,
            ret['error'] = '获取数据失败'

        # print(ret.get('data'))

        return Response(ret)



