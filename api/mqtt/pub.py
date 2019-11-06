"""
接收设备数据，如果设备存在则收到的数据存入deviceData表中，如果不存在则创建设备到deviceInfo中
"""
import time

import paho.mqtt.client as mqtt


# 绑定 MQTT 服务器地址
# MQTT服务器的端口号
BORKER = '127.0.0.1'
PORT = 1883
client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
client = mqtt.Client(client_id)


# 启动函数
def mqtt_run():
    client.connect(BORKER, PORT, 60)
    # client.username_pw_set('user', 'user')
    client.reconnect_delay_set(min_delay=1, max_delay=2000)
    # 网络循环的函数
    client.loop_forever(retry_first_connection=False)


# publish 消息
def on_publish(topic, payload, qos):
    client.publish(topic, payload, qos)


if __name__ == "__main__":
    mqtt_run()
