"""
接收设备数据，如果设备存在则收到的数据存入deviceData表中，如果不存在则创建设备到deviceInfo中
"""
import time

import paho.mqtt.client as mqtt

from api.views.deviceData import PostData

# 绑定 MQTT 服务器地址
# MQTT服务器的端口号
BORKER = '127.0.0.1'
PORT = 1883


# 启动函数
def mqtt_run():
    client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BORKER, PORT, 60)
    # on_publish("868995039003043", "Hello Python!", 0)
    # client.username_pw_set('user', 'user')
    client.reconnect_delay_set(min_delay=1, max_delay=2000)
    # 网络循环的函数
    client.loop_forever(retry_first_connection=False)


# 建立mqtt连接
def on_connect(client, userdata, flag, rc):
    print("mqtt服务器连接状态 " + str(rc))
    client.subscribe('ipmPub', 0)


# 接收、处理mqtt消息
def on_message(client, userdata, msg):
    out = str(msg.payload.decode('utf-8'))
    if msg.topic == 'ipmPub':
        send = PostData()
        send.post(out)


# publish 消息
def on_publish(topic, payload, qos):

    client.publish(topic, payload, qos)


# mqtt客户端启动函数
# def mqttfunction():
#     # 使用loop_start 可以避免阻塞Django进程，使用loop_forever()可能会阻塞系统进程
#     # client.loop_start()
#     # client.loop_forever() 有掉线重连功能
#     client.loop_forever(retry_first_connection=False)


# 启动 MQTT
# mqtt_run()


if __name__ == "__main__":
    mqtt_run()
