# Generated by Django 2.2.7 on 2020-02-27 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0014_usertoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(0, '普通用户'), (1, '管理员')]),
        ),
    ]
