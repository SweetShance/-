# Generated by Django 2.2 on 2020-03-31 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataManagement', '0008_auto_20200330_1107'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicationform',
            old_name='etcImage',
            new_name='cetImage',
        ),
    ]
