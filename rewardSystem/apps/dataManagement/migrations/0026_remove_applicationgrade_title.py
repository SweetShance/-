# Generated by Django 2.2 on 2020-04-10 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataManagement', '0025_auto_20200410_2127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationgrade',
            name='title',
        ),
    ]