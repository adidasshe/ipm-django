from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class DeviceInfo(models.Model):
    device_id = models.CharField(max_length=128,unique= True)
    device_name = models.CharField(max_length=64)
    device_desc = models.CharField(max_length=128)
    longitude = models.FloatField()
    latitude = models.FloatField()
    address = models.CharField(max_length=256)
    soft_version = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)


class DeviceData(models.Model):
    device_id = models.ForeignKey("DeviceInfo",on_delete=models.CASCADE)
    voltage1 = models.FloatField()
    voltage2 = models.FloatField()
    voltage3 = models.FloatField()
    current1 = models.FloatField()
    current2 = models.FloatField()
    current3 = models.FloatField()
    leakage_current1 = models.FloatField()
    leakage_current2 = models.FloatField()
    leakage_current3 = models.FloatField()
    switch1 = models.IntegerField()
    switch2 = models.IntegerField()
    switch3 = models.IntegerField()
    unbalanced_state1 = models.FloatField()
    power_factor1 = models.FloatField()
    capacitance_switch1 = models.IntegerField(null=True,default=0)
    capacitance_switch2 = models.IntegerField(null=True,default=0)
    capacitance_switch3 = models.IntegerField(null=True,default=0)
    capacitance_switch4 = models.IntegerField(null=True,default=0)
    capacitance_switch5 = models.IntegerField(null=True,default=0)
    capacitance_switch6 = models.IntegerField(null=True,default=0)
    capacitance_switch7 = models.IntegerField(null=True,default=0)
    capacitance_switch8 = models.IntegerField(null=True,default=0)
    capacitance_switch9 = models.IntegerField(null=True,default=0)
    capacitance_switch10 = models.IntegerField(null=True,default=0)
    capacitance_switch11 = models.IntegerField(null=True,default=0)
    capacitance_switch12 = models.IntegerField(null=True,default=0)
    capacitance_switch13 = models.IntegerField(null=True,default=0)
    capacitance_switch14 = models.IntegerField(null=True,default=0)
    capacitance_switch15 = models.IntegerField(null=True,default=0)
    capacitance_switch16 = models.IntegerField(null=True,default=0)
    capacitance_switch17 = models.IntegerField(null=True,default=0)
    capacitance_switch18 = models.IntegerField(null=True,default=0)
    power_switch1 = models.IntegerField(null=True,default=0)
    power_switch2 = models.IntegerField(null=True,default=0)
    power_switch3 = models.IntegerField(null=True,default=0)
    power_switch4 = models.IntegerField(null=True,default=0)
    power_switch5 = models.IntegerField(null=True,default=0)
    power_switch6 = models.IntegerField(null=True,default=0)
    power_switch7 = models.IntegerField(null=True,default=0)
    power_switch8 = models.IntegerField(null=True,default=0)
    power_switch9 = models.IntegerField(null=True,default=0)
    date = models.DateTimeField(auto_now_add=True)


class Control(models.Model):
    date = models.DateTimeField(primary_key=True,auto_now_add=True)
    device_id = models.ForeignKey("DeviceInfo",on_delete=models.CASCADE)
    operator = models.CharField(max_length=64)
    switch_set1 = models.IntegerField(blank=True, null=True)
    switch_set2 = models.IntegerField(blank=True, null=True)
    switch_set3 = models.IntegerField(blank=True, null=True)
    leakage_current_set1 = models.FloatField(blank=True, null=True)
    leakage_current_set2 = models.FloatField(blank=True, null=True)
    leakage_current_set3 = models.FloatField(blank=True, null=True)
    power_factor_set1 = models.FloatField(blank=True, null=True)
    switch_delay_set1 = models.FloatField(blank=True, null=True)
    ct_var_value = models.FloatField(blank=True, null=True)



class Value(models.Model):
    device_id = models.OneToOneField("DeviceInfo",on_delete=models.CASCADE)
    switch_set1 = models.IntegerField(blank=True, null=True)
    switch_set2 = models.IntegerField(blank=True, null=True)
    switch_set3 = models.IntegerField(blank=True, null=True)
    leakage_current_set1 = models.FloatField(blank=True, null=True)
    leakage_current_set2 = models.FloatField(blank=True, null=True)
    leakage_current_set3 = models.FloatField(blank=True, null=True)
    power_factor_set1 = models.FloatField(blank=True, null=True)
    switch_delay_set1 = models.FloatField(blank=True, null=True)
    ct_var_value = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)




class Register(models.Model):
    """
    用户表
    """
    prop = (
        (0, "superAdmin"),
        (1, "admin"),
        (2, "user"),
    )
    sex = (
        (1,"男"),
        (2,"女"),
    )
    username = models.CharField(max_length=64,unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    prop = models.IntegerField(choices=prop,blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    sex = models.IntegerField(choices=sex,blank=True, null=True)
    age = models.CharField(max_length=10,blank=True, null=True,)
    company = models.CharField( max_length=50, blank=True, null=True)
    duty = models.CharField( max_length=50, blank=True, null=True)
    phone = models.CharField( max_length=11, blank=True, null=True)
    desc = models.CharField( max_length=150, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)



class UserToken(models.Model):
    """用户token认证表"""
    user = models.OneToOneField("Register",on_delete= models.CASCADE)
    token = models.CharField(max_length=64)

# class UserProp(models.Model):
#     """用户权限表"""
#     prop = models.CharField(max_length=10)
#
# class UserSex(models.Model):
#     """用户性别表"""
#     sex = models.CharField(max_length=10)



