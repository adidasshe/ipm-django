import time

from api import models
from api.auth.auth import Auth
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
import json
import math

"""设备数据序列化类
"""


class DataSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(source='device_id.device_id')
    # 设置日期格式化格式
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = models.DeviceData
        # fields = ['device_id','voltage1','voltage2','voltage3','device']
        fields = "__all__"
        # depth = 0


"""
上传数据操作
"""


class DeviceDataView(APIView):
    authentication_classes = [Auth, ]

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'data': None}
        # print(request.query_params)
        device_id = request.query_params.get('data')
        # device_id = '868995039003043'
        try:
            if len(device_id) == 0:
                ret['code'] = 1003,
                ret['error'] = '请选择需要查看的设备'
            else:
                obj = models.DeviceInfo.objects.filter(device_id=device_id).first()
                # print(id.values())
                # data = models.DeviceData.objects.filter(device_id=id).order_by('id').reverse()[:1]
                # 外键反向关联查询
                data = obj.devicedata_set.all().order_by('id').reverse()[:1]
                if data.exists():
                    ser = DataSerializer(instance=data, many=True)
                    ret['data'] = ser.data
                else:
                    ret['code'] = 1002,
                    ret['error'] = '该设备未上传数据'
        except Exception as e:
            print(e)
            ret['code'] = 1001,
            ret['error'] = '获取数据失败'
        print(ret.get('code'))
        # print(ret.get('data'))
        return Response(ret)


# mqtt客户端收到消息写入数据库
class PostData():
    # def handler(self,data):
    #
    #     ret = {'device_id':device_id,'data':data}
    #     return ret
    def post(self, data):
        try:
            # print(data)
            str = data.split('@data')
            # 上传消息的设备号
            device_id = str[0]
            resTime = int(time.time())
            # print(resTime)
            data = json.loads(str[1])
            obj = models.DeviceInfo.objects.filter(device_id=device_id).first()

            def handleData():
                nonlocal data
                lc1 = "%.2f" % (1000 * math.sqrt(data['lc1'] / 20) * 3.3 / 4096 * 2)
                # print(lc1)
                lc2 = "%.2f" % (1000 * math.sqrt(data['lc2'] / 20) * 3.3 / 4096 * 2)
                # print(lc2)
                lc3 = "%.2f" % (1000 * math.sqrt(data['lc3'] / 20) * 3.3 / 4096 * 2)
                # print(type(lc1))
                # 漏电值小于setValue 的清零处理
                setValue = 20.00
                if float(lc1) < setValue:
                    lc1 = 0
                if float(lc2) < setValue:
                    lc2 = 0
                if float(lc3) < setValue:
                    lc3 = 0
                models.DeviceData.objects.create(device_id=obj,
                                                 voltage1=data['v1'] / 10,
                                                 voltage2=data['v2'] / 10,
                                                 voltage3=data['v3'] / 10,
                                                 current1=data['c1'] / 10,
                                                 current2=data['c2'] / 10,
                                                 current3=data['c3'] / 10,
                                                 leakage_current1=lc1,
                                                 leakage_current2=lc2,
                                                 leakage_current3=lc3,
                                                 switch1=data['s1'],
                                                 switch2=data['s2'],
                                                 switch3=data['s3'],
                                                 unbalanced_state1=int(data['us']) / 100,
                                                 power_factor1=int(data['pf1']) / 1000,
                                                 capacitance_switch1=int(data['cs'] >> 0) & 1,
                                                 capacitance_switch2=int(data['cs'] >> 1) & 1,
                                                 capacitance_switch3=int(data['cs'] >> 2) & 1,
                                                 capacitance_switch4=int(data['cs'] >> 3) & 1,
                                                 capacitance_switch5=int(data['cs'] >> 4) & 1,
                                                 capacitance_switch6=int(data['cs'] >> 5) & 1,
                                                 capacitance_switch7=int(data['cs'] >> 6) & 1,
                                                 capacitance_switch8=int(data['cs'] >> 7) & 1,
                                                 capacitance_switch9=int(data['cs'] >> 8) & 1,
                                                 capacitance_switch10=int(data['cs'] >> 9) & 1,
                                                 capacitance_switch11=int(data['cs'] >> 10) & 1,
                                                 capacitance_switch12=int(data['cs'] >> 11) & 1,
                                                 capacitance_switch13=int(data['cs'] >> 12) & 1,
                                                 capacitance_switch14=int(data['cs'] >> 13) & 1,
                                                 capacitance_switch15=int(data['cs'] >> 14) & 1,
                                                 capacitance_switch16=int(data['cs'] >> 15) & 1,
                                                 capacitance_switch17=int(data['cs'] >> 16) & 1,
                                                 capacitance_switch18=int(data['cs'] >> 17) & 1,
                                                 power_switch1=int(data['ps'] >> 0) & 3,
                                                 power_switch2=int(data['ps'] >> 2) & 3,
                                                 power_switch3=int(data['ps'] >> 4) & 3,
                                                 power_switch4=int(data['ps'] >> 6) & 3,
                                                 power_switch5=int(data['ps'] >> 8) & 3,
                                                 power_switch6=int(data['ps'] >> 10) & 3,
                                                 power_switch7=int(data['ps'] >> 12) & 3,
                                                 power_switch8=int(data['ps'] >> 14) & 3,
                                                 power_switch9=int(data['ps'] >> 16) & 3
                                                 )

            if obj:
                # date = models.DeviceData.objects.filter(device_id=obj).order_by('id').reverse()[:1]
                # if date.exists():
                #     date = DataSerializer(instance=date, many=True)
                #     times = date.data[0].get('date')
                #     timeArray = time.strptime(times, "%Y-%m-%d %H:%M:%S")
                #     # 拿到该设备开关上一条指令发送的时间戳
                #     timeStamp = int(time.mktime(timeArray))
                #     # print(timeStamp)
                #     interval = resTime - timeStamp
                #     if interval < 2:
                #         # 如果上次的写入数据库时间跟现在接收时间少于2秒则认为是多线程重复处理的数据不予写入数据库
                #         pass
                #     else:
                handleData()
            else:
                models.DeviceInfo.objects.create(device_id=device_id,
                                                 device_name=device_id,
                                                 longitude=data['lnt'],
                                                 latitude=data['lat'],
                                                 soft_version=data['sv'],
                                                 )
                handleData()

        except Exception as e:
            print(e)
            return resTime
