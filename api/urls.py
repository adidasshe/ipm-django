#API配置
from django.urls import re_path
from api.views import views, user, changePass, logout, getProp, getUser, getDevice, deviceData, deviceInfo, control, \
    account, value, mapData


urlpatterns = [
    re_path(r'(?P<version>[v1|v2]+)/user/', user.UserView.as_view()),
    re_path(r'(?P<version>[v1|v2]+)/device_data/',deviceData.DeviceDataView.as_view()),
    re_path(r'(?P<version>[v1|v2]+)/control/', control.ControlView.as_view()),
    re_path(r'(?P<version>[v1|v2]+)/device_info/', deviceInfo.DeviceInfoView.as_view()),
    re_path(r'(?P<version>[v1|v2]+)/auth/', account.AuthView.as_view()),
    re_path(r'(?P<version>[v1|v2]+)/logout/', logout.Logout.as_view()),
    re_path(r'(?P<version>[v1|v2]+)/changePass/', changePass.ChangePass.as_view()),
    re_path(r'(?P<version>[v1|v2]+)/roles/', getProp.GetProp.as_view()),
    re_path(r'(?P<version>[v1|v2]+)/getUser/', getUser.GetUserView.as_view()),
    re_path(r'(?P<version>[v1|v2]+)/getDevice/', getDevice.GetDeviceView.as_view()),
    re_path(r'(?P<version>[v1|v2]+)/value/', value.ValueView.as_view()),
    re_path(r'(?P<version>[v1|v2]+)/map/', mapData.MapDataView.as_view()),
]
