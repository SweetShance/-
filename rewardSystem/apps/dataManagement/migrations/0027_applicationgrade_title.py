# Generated by Django 2.2 on 2020-04-11 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataManagement', '0026_remove_applicationgrade_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationgrade',
            name='title',
            field=models.CharField(default=1, max_length=100, verbose_name='赋分项'),
            preserve_default=False,
        ),
    ]