# Generated by Django 2.2 on 2020-04-17 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyUser', '0002_usercode'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercode',
            name='email',
            field=models.EmailField(default='2391454874@qq.com', max_length=254, verbose_name='邮箱'),
            preserve_default=False,
        ),
    ]