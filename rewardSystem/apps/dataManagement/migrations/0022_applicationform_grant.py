# Generated by Django 2.2 on 2020-04-16 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataManagement', '0021_auto_20200416_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationform',
            name='grant',
            field=models.ManyToManyField(blank=True, related_name='other_grant', to='dataManagement.GrantLevel', verbose_name='其他奖助'),
        ),
    ]
