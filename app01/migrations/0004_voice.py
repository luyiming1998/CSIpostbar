# Generated by Django 2.2.7 on 2020-02-22 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_user_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auSetVol', models.IntegerField()),
                ('auSetVoiper', models.IntegerField()),
                ('auSetSpd', models.IntegerField()),
                ('auSetPit', models.IntegerField()),
            ],
        ),
    ]
