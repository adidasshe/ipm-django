from api import models
from api.auth.auth import Auth
from api.models import Control
import time
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
# from api.mqtt.mqttClient import on_publish
import paho.mqtt.publish as publish

"""
操作信息序列化类
"""
BORKER = '127.0.0.1'
PORT = 1883


class ControlSerializer(serializers.ModelSerializer):
    # 设置日期格式化格式
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = models.Control
        fields = "__all__"


"""
操作下发
"""


class ControlView(APIView):
    authentication_classes = [Auth, ]

    def get(self, request, *args, **kwargs):
        control = Control.objects.all().first()
        ser = ControlSerializer(instance=control, many=False)
        ser.data
        return Response(ser.data)

    def post(self, request, *args, **kwargs):
        print(request.data)
        ret = {'code': 1000, 'success': '', 'data': None}
        operator = request.data.get('name')
        device_id = request.data.get('device_id')
        switch1 = request.data.get('switch1')
        switch2 = request.data.get('switch2')
        switch3 = request.data.get('switch3')
        leakage1 = request.data.get('leakage1')
        leakage2 = request.data.get('leakage2')
        leakage3 = request.data.get('leakage3')
        ct = request.data.get('ct')
        power = request.data.get('power')

        # print(type(switch2))
        def pubSwitch(request):
            operator = request.data.get('name')
            device_id = request.data.get('device_id')
            switch1 = request.data.get('switch1')
            switch2 = request.data.get('switch2')
            switch3 = request.data.get('switch3')
            leakage1 = request.data.get('leakage1')
            leakage2 = request.data.get('leakage2')
            leakage3 = request.data.get('leakage3')
            ct = request.data.get('ct')
            power = request.data.get('power')
            # 将操作写入数据库
            models.Control.objects.create(device_id=obj,
                                          operator=operator, switch_set1=switch1, switch_set2=switch2,
                                          switch_set3=switch3,
                                          )
            # 向设备发送开关操作
            # 整理数据成字符串！！！
            midder = 'devcrl@'
            # 此为预留值
            switch_delay = 800
            leakage1 = int(pow(4096 * leakage1 / 6.6, 2) * 20 / 1000000)
            leakage2 = int(pow(4096 * leakage2 / 6.6, 2) * 20 / 1000000)
            leakage3 = int(pow(4096 * leakage3 / 6.6, 2) * 20 / 1000000)
            sendData = midder + str(switch1) + "," + str(switch2) + "," + str(
                switch3) + "," + str(leakage1) + "," + str(leakage2) + "," + str(
                leakage3) + "," + str(int(100 * power)) + "," + str(switch_delay) + "," + str(ct)

            print(sendData)
            # on_publish(device_id,"0,0,868995039003043,devcrl@1,0,0,1232486,308121,19719776,100,800,30",0)
            # 调用MQTT客户端发布主题方法
            # on_publish(device_id, sendData, 0)
            publish.single(device_id, sendData, hostname=BORKER)

        try:
            obj = models.DeviceInfo.objects.filter(device_id=device_id).first()
            # print(obj)
            if obj:
                if switch1 == 1:
                    # 如果下发的是开关1操作
                    # 判断上次操作该开关时间
                    # date = obj.control_set.all().order_by('date').reverse()[:1]
                    date = models.Control.objects.filter(device_id=obj, switch_set1=1).order_by('date').reverse()[:1]
                    if date.exists():
                        date = ControlSerializer(instance=date, many=True)
                        print(date.data)
                        times = date.data[0].get('date')
                        timeArray = time.strptime(times, "%Y-%m-%d %H:%M:%S")
                        # 拿到该设备开关上一条指令发送的时间戳
                        timeStamp = int(time.mktime(timeArray))
                        # print(timeStamp)
                        # 当前时间戳
                        now = int(time.time())
                        # print(now)
                        # 时间间隔
                        interval = 300
                        # 如果同一开关下发时间间隔interval小于5分钟则不允许再次下发
                        if now - timeStamp < interval:
                            intervalTime = interval - (now - timeStamp)
                            print(intervalTime)
                            ret['code'] = 1004
                            ret['error'] = "请" + str(intervalTime) + ":秒后再下发开关1操作"
                        else:
                            pubSwitch(request)
                            ret['success'] = '成功下发开关1'
                    else:
                        pubSwitch(request)
                        ret['success'] = '成功下发开关1'
                elif switch2 == 1:
                    # 如果下发的是开关2操作
                    # 判断上次操作该开关时间
                    date = models.Control.objects.filter(device_id=obj, switch_set2=1).order_by('date').reverse()[:1]
                    if date.exists():
                        date = ControlSerializer(instance=date, many=True)
                        times = date.data[0].get('date')
                        timeArray = time.strptime(times, "%Y-%m-%d %H:%M:%S")
                        # 拿到该设备开关上一条指令发送的时间戳
                        timeStamp = int(time.mktime(timeArray))
                        # print(timeStamp)
                        # 当前时间戳
                        now = int(time.time())
                        # print(now)
                        # 时间间隔
                        interval = 300
                        # 如果同一开关下发时间间隔interval小于5分钟则不允许再次下发
                        if now - timeStamp < interval:
                            intervalTime = interval - (now - timeStamp)
                            print(intervalTime)
                            ret['code'] = 1004
                            ret['error'] = "请" + str(intervalTime) + ":秒后再下开关2操作"
                        else:
                            pubSwitch(request)
                            ret['success'] = '成功下发开关2'
                    else:
                        pubSwitch(request)
                        ret['success'] = '成功下发开关2'

                elif switch3 == 1:
                    # 如果下发的是开关3操作
                    # 判断上次操作该开关时间
                    date = models.Control.objects.filter(device_id=obj, switch_set3=1).order_by('date').reverse()[:1]
                    if date.exists():
                        date = ControlSerializer(instance=date, many=True)
                        times = date.data[0].get('date')
                        timeArray = time.strptime(times, "%Y-%m-%d %H:%M:%S")
                        # 拿到该设备开关上一条指令发送的时间戳
                        timeStamp = int(time.mktime(timeArray))
                        # print(timeStamp)
                        # 当前时间戳
                        now = int(time.time())
                        # print(now)
                        # 时间间隔
                        interval = 300
                        # 如果同一开关下发时间间隔interval小于5分钟则不允许再次下发
                        if now - timeStamp < interval:
                            intervalTime = interval - (now - timeStamp)
                            print(intervalTime)
                            ret['code'] = 1004
                            ret['error'] = "请" + str(intervalTime) + ":秒后再下开关3操作"
                        else:
                            pubSwitch(request)
                            ret['success'] = '成功下发开关3'
                    else:
                        pubSwitch(request)
                        ret['success'] = '成功下发开关3'
                else:
                    # 如果下发的是阈值操作
                    # 下发到设备操作表
                    models.Control.objects.create(device_id=obj,
                                                  operator=operator,
                                                  leakage_current_set1=leakage1, leakage_current_set2=leakage2,
                                                  leakage_current_set3=leakage3,
                                                  power_factor_set1=power,
                                                  ct_var_value=ct,
                                                  )
                    # 更新设备阈值表
                    models.Value.objects.update_or_create(device_id=obj,
                                                          defaults={'leakage_current_set1': leakage1,
                                                                    'leakage_current_set2': leakage2,
                                                                    'leakage_current_set3': leakage3,
                                                                    'power_factor_set1': power,
                                                                    'ct_var_value': ct, }
                                                          )
                    # 向设备发送阈值操作
                    # 整理数据成字符串！！！
                    midder = 'devcrl@'
                    # 此为预留值
                    switch_delay = 800
                    leakage1 = int(pow(4096 * leakage1 / 6.6, 2) * 20 / 1000000)
                    leakage2 = int(pow(4096 * leakage2 / 6.6, 2) * 20 / 1000000)
                    leakage3 = int(pow(4096 * leakage3 / 6.6, 2) * 20 / 1000000)
                    sendData = midder + str(switch1) + "," + str(switch2) + "," + str(
                        switch3) + "," + str(leakage1) + "," + str(leakage2) + "," + str(
                        leakage3) + "," + str(int(100 * power)) + "," + str(switch_delay) + "," + str(ct)
                    print(sendData)
                    # on_publish(device_id,"0,0,868995039003043,devcrl@1,0,0,1232486,308121,19719776,100,800,30",0)
                    # 调用MQTT客户端发布主题方法
                    publish.single(device_id, sendData, hostname=BORKER)
                    ret['success'] = '成功下发阈值'
            else:
                # print("333")
                ret['code'] = 1002
                ret['error'] = '设备不存在'
        except Exception as e:
            print(e)
            ret['code'] = 1003
            ret['error'] = '下发失败'
        print(ret.get('code'))
        return Response(ret)
