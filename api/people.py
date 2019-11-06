# class People:
#     name = ""
#     age = 18
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#     def speak(self):
#         print("%s 说: 我 %d 岁。" % (self.name, self.age))
#     def eat(self):
#         print("%s 吃饭！" %(self.name))
#
#
# class Student(People):
#     # def eat(self):
#     #     print("我是学生类的吃饭方法！")
#     def study(self):
#         print("%s 在学习" %(self.name))
#     pass
#
# class Ppp(Student):
#     pass
#
# # p = Ppp("小民",19)
# # p.speak()
#
#
#
# import re
# # a = re.compile(r'\d+')
# # a.findall('one1two2three3four4')
# # print(a.findall('one1two2three3four4'))
#
# a =re.findall(r'\d+','one1two2three3four4')
# print(a)
a = 3648

print((a>>0)&3)
print((a>>2)&3)
print((a>>4)&3)
print((a>>6)&3)
print((a>>8)&3)
print((a>>10)&3)