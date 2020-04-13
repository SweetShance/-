from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class MyUser(AbstractUser):
    name = models.CharField(max_length=20, verbose_name="姓名", blank=True, null=True)
    phone = models.CharField(max_length=11, verbose_name="电话", blank=True, null=True)
    IDENTITY = [
        ("学生", "学生"),
        ("老师", "老师"),
        ("管理员", "管理员")
    ]
    identity = models.CharField(verbose_name="身份", max_length=10, choices=IDENTITY, default="学生")

    class Meta:
        verbose_name_plural = "用户"

    def __str__(self):
        return "%s"%self.name