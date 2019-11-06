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

def server_conenet(client):
    client.on_connect = on_connect  # 启用订阅模式
    client.on_message = on_message  # 接收消息
    client.connect(BORKER, PORT, 60)  # 链接
    # client.loop_start()   # 以start方式运行，需要启动一个守护线程，让服务端运行，否则会随主线程死亡
    client.loop_forever()  # 以forever方式阻塞运行。


# 启动函数
def mqtt_run():
    client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    client = mqtt.Client(client_id, transport='tcp')
    # client.username_pw_set('user', 'user')
    server_conenet(client)





if __name__ == "__main__":
    mqtt_run()
