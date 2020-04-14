# Generated by Django 2.2 on 2020-04-14 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataManagement', '0006_remove_jury_all_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='jury',
            name='all_status',
            field=models.CharField(choices=[('未提交', '未提交'), ('已提交', '已提交')], default='未提交', max_length=3, verbose_name='全部是否提交'),
        ),
    ]