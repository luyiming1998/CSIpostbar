# Generated by Django 2.2.7 on 2020-02-24 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0010_auto_20200224_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='status',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='comment',
            name='support',
            field=models.IntegerField(default=0),
        ),
    ]