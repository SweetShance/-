from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class MyUser(AbstractUser):
    name = models.CharField(max_length=20, verbose_name="姓名", blank=True, null=True)
    phone = models.CharField(max_length=11, verbose_name="电话", blank=True, null=True)
    IDENTITY = [
        ("学生", "学生"),
        ("老师", "老师"),
        ("评委", "评委"),
        ("管理员", "管理员")
    ]
    identity = models.CharField(verbose_name="身份", max_length=10, choices=IDENTITY, default="学生")

    class Meta:
        verbose_name_plural = "用户"

    def __str__(self):
        return "%s"%self.name


class UserCode(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=20)
    email = models.EmailField(verbose_name="邮箱")
    code = models.CharField(verbose_name="验证码", max_length=10)
    date = models.DateTimeField(verbose_name="时间", auto_now_add=True)