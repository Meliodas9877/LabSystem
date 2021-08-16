from django.db import models

# Create your models here.
class student2 ( models.Model ):
    studentId = models.CharField ( max_length=12, null=False, blank=True, verbose_name='学号',primary_key=True )
    studentName = models.CharField ( max_length=50,null=True, blank=True, verbose_name='姓名' )
    gender = models.CharField ( max_length=1,null=True, verbose_name='性别' )
    schoolYear = models.CharField ( max_length=4, null=True, blank=True, verbose_name='入学年份' )
    telephone = models.CharField ( max_length=11, null=True, blank=True, verbose_name='手机号' )
    email = models.CharField ( max_length=50, null=True, blank=True, verbose_name='邮箱' )
    studentType = models.CharField ( max_length=2, null=True, blank=True, verbose_name='学生类别' )
    idNo = models.CharField ( max_length=18, null=True, blank=True, verbose_name='身份证号' )
    password = models.CharField ( max_length=50, null=True, blank=True, verbose_name='密码' )
    avatarUrl = models.CharField ( max_length=4000, null=True, blank=True, verbose_name='头像地址' )