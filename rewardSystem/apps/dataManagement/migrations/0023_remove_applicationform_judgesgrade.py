# Generated by Django 2.2 on 2020-04-16 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataManagement', '0022_applicationform_grant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationform',
            name='judgesGrade',
        ),
    ]