# Generated by Django 2.2.7 on 2020-02-24 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0009_auto_20200224_1034'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='article',
            new_name='cm_article',
        ),
        migrations.AddField(
            model_name='comment',
            name='cm_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app01.User'),
            preserve_default=False,
        ),
    ]
