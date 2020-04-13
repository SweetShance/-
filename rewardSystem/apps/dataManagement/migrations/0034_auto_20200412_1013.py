# Generated by Django 2.2 on 2020-04-12 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataManagement', '0033_notice'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='content',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='内容'),
        ),
        migrations.CreateModel(
            name='NoticeFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='notice', verbose_name='文件')),
                ('notice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notice_files', to='dataManagement.Notice')),
            ],
            options={
                'verbose_name': '公告文件',
                'verbose_name_plural': '公告文件',
            },
        ),
    ]