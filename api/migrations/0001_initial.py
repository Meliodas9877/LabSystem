# Generated by Django 3.1.3 on 2021-08-16 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='student2',
            fields=[
                ('studentId', models.CharField(blank=True, max_length=12, primary_key=True, serialize=False, verbose_name='学号')),
                ('studentName', models.CharField(blank=True, max_length=50, null=True, verbose_name='姓名')),
                ('gender', models.CharField(max_length=1, null=True, verbose_name='性别')),
                ('schoolYear', models.CharField(blank=True, max_length=4, null=True, verbose_name='入学年份')),
                ('telephone', models.CharField(blank=True, max_length=11, null=True, verbose_name='手机号')),
                ('email', models.CharField(blank=True, max_length=50, null=True, verbose_name='邮箱')),
                ('studentType', models.CharField(blank=True, max_length=2, null=True, verbose_name='学生类别')),
                ('idNo', models.CharField(blank=True, max_length=18, null=True, verbose_name='身份证号')),
                ('password', models.CharField(blank=True, max_length=50, null=True, verbose_name='密码')),
                ('avatarUrl', models.CharField(blank=True, max_length=4000, null=True, verbose_name='头像地址')),
            ],
        ),
    ]
