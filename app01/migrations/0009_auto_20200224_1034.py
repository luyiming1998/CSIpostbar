# Generated by Django 2.2.7 on 2020-02-24 02:34

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0008_auto_20200224_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.expressions.Case, to='app01.User'),
            preserve_default=False,
        ),
    ]
