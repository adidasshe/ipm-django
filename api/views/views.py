
# # #执行mqtt脚本，独立线程运行，接收管控仪发布的主题
from api.mqtt.sub import mqtt_run
from threading import Thread

mqttThread1 = Thread(target=mqtt_run)
mqttThread1.start()



