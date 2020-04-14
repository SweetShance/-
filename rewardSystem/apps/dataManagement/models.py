from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.db.models.signals import pre_delete #删除文件
from django.dispatch.dispatcher import receiver #删除文件
from django.forms import fields
from MyUser.models import MyUser
# Create your models here.


class Student(models.Model):
    sno = models.CharField(max_length=12, verbose_name="学号")
    sname = models.CharField(max_length=20, verbose_name="姓名")
    S_SEX = [
        ("男", "男"),
        ("女", "女")
    ]
    sex = models.CharField(max_length=2, verbose_name="性别", choices=S_SEX, default="", null=True, blank=True)
    startDate = models.DateField(verbose_name="入学年月", default=timezone.now)
    tutor = models.ForeignKey('Teacher', verbose_name="导师", on_delete=models.DO_NOTHING, blank=True, null=True, related_name="student_teacher")
    CET4Count = models.SmallIntegerField(verbose_name="四级使用次数", default=0)
    CET6Count = models.SmallIntegerField(verbose_name="六级使用次数", default=0)
    registerStatus = models.BooleanField(verbose_name="是否注册用户", default=False)
    AdmissionStatus_CHOICE = [
        ("自考", '自考'),
        ("推免", "推免")
    ]
    admissionstatus = models.CharField(verbose_name="入学身份", max_length=20, default='自考')
    # status = models.BooleanField(verbose_name="申请资格", default=True)

    class Meta:
        verbose_name = "学生"
        verbose_name_plural = "学生"

    def __str__(self):
        return "%s"%self.sname


class Teacher(models.Model):
    tno = models.CharField(max_length=12, verbose_name="工号")
    tname = models.CharField(max_length=20, verbose_name="姓名")
    S_SEX = [
        ("男", "男"),
        ("女", "女")
    ]
    sex = models.CharField(max_length=2, verbose_name="性别", choices=S_SEX, default="", null=True, blank=True)
    register_status = models.BooleanField(verbose_name="是否注册用户", default=False)

    class Meta:
        verbose_name = "老师"
        verbose_name_plural = "老师"

    def __str__(self):
        return "%s"%self.tname


# 评委
class Jury(models.Model):
    meeting = models.ForeignKey('Meeting', verbose_name="会议", on_delete=models.CASCADE, related_name="meeting_jury")
    jno = models.CharField(max_length=20, verbose_name="用户名")
    jname = models.CharField(max_length=20, verbose_name="姓名")
    password = models.CharField(max_length=20, verbose_name="密码")
    user_id = models.IntegerField(verbose_name="用户id", blank=True, null=True)
    # chief_umpire_status = models.BooleanField(verbose_name="主审是否提交", default=False)
    CHOICE = [
        ("未提交", "未提交"),
        ("已提交", "已提交")
    ]
    all_status = models.CharField(verbose_name="全部是否提交", max_length=3, choices=CHOICE, default="未提交")

    class Meta:
        verbose_name = "评委"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s"%self.jname


# 赋分表
class FuTable(models.Model):
    title = models.CharField(verbose_name="赋分表名称", max_length=20)

    class Meta:
        verbose_name = "赋分表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s"%self.title


# 赋分项
class AssignItem(models.Model):
    fuTable = models.ForeignKey(FuTable, on_delete=models.CASCADE, related_name="fuItem")
    title = models.CharField(verbose_name="赋分项", max_length=50)
    grade = models.IntegerField(verbose_name="分数")
    scoring = models.TextField(verbose_name="赋分标准", max_length=300)
    state = models.TextField(verbose_name="说明", max_length=300)
    show = models.BooleanField(verbose_name="是否让评委为其赋分", default=True)

    class Meta:
        verbose_name = "赋分项列表"
        verbose_name_plural = verbose_name


# 申请表
class ApplicationForm(models.Model):
    student = models.ForeignKey(Student, verbose_name="学生", on_delete=models.CASCADE, related_name="student_applicationform")
    sno = models.CharField(max_length=11, verbose_name="学生学号")
    sname = models.CharField(max_length=20, verbose_name="学生姓名")
    presentation = models.TextField(max_length=500, verbose_name="学生简介")
    # baseGrade = models.SmallIntegerField(verbose_name="基本分", default=10)
    CET_CHOICE = [
        ('四级', '四级'),
        ('六级', '六级')
    ]

    englishChoice = models.CharField(max_length=2, verbose_name="四级/六级", choices=CET_CHOICE, default="四级")
    cetImage = models.ImageField(verbose_name="四级/六级图片", upload_to='ETCImage', blank=True)
    cetstatus = models.BooleanField(verbose_name="使用状态", default=False)
    # englishGrade = models.IntegerField(verbose_name="四级/六级分数")
    # 学术活动
    academicActivityText = models.CharField(verbose_name="参与学术活动介绍", max_length=500)
    # academicActivityGrade = models.SmallIntegerField(verbose_name="学术活动分数", null=True, blank=True)
    # 发表论文
    publicationsText = models.CharField(verbose_name="发表论文介绍", max_length=500)
    # publicationsGrade = models.SmallIntegerField(verbose_name="发表论文分数", null=True, blank=True)
    # 参与项目
    participateItemsText = models.CharField(verbose_name="参与项目介绍", max_length=500)
    # participateItemsGrade = models.SmallIntegerField(verbose_name="参与项目分数", null=True, blank=True)
    # 科研项目
    researchProjectsText = models.CharField(verbose_name="科研项目介绍", max_length=500)
    # researchProjectsGrade = models.SmallIntegerField(verbose_name="科研项目分数", null=True, blank=True)
    # 研究生创新项目
    innovationProjectsText = models.CharField(verbose_name="研究生创新项目介绍", max_length=500)
    # innovationProjectsGrade = models.SmallIntegerField(verbose_name="研究生创新项目分数", null=True, blank=True)
    # 社会服务
    socialWorkText = models.CharField(verbose_name="社会服务介绍", max_length=500)
    # socialWorkGrade = models.SmallIntegerField(verbose_name="社会服务分数", null=True, blank=True)
    # mentorGrade = models.SmallIntegerField(verbose_name="导师评分", null=True, blank=True)
    # otherGrade = models.SmallIntegerField(verbose_name="学生评分", null=True, blank=True)
    # 学生互评
    otherstatus = models.BooleanField(verbose_name="是否被评分", default=False)
    tootherstatus = models.BooleanField(verbose_name="是否评分", default=False)
    judgesGrade = models.SmallIntegerField(verbose_name="评委赋分", null=True, blank=True)
    upload_time = models.DateTimeField(verbose_name="提交时间", auto_now_add=True)
    # evaluate = models.TextField(verbose_name="说明", max_length=200)
    # 等级
    grant = models.ForeignKey('GrantLevel', verbose_name="等级", on_delete=models.CASCADE, null=True)
    # 导师审核
    # activity = models.BooleanField(verbose_name="是否通过审核", default=False)

    activity = models.BooleanField(verbose_name="导师审核状态", default=False)
    jury = models.ForeignKey(Jury, verbose_name="主审评委", on_delete=models.DO_NOTHING, null=True, blank=True)
    # 会议
    meeting = models.ForeignKey('Meeting', verbose_name="所属会议", on_delete=models.CASCADE, related_name="meeting_for_applicationform")
    # 赋分表
    fuTable = models.ForeignKey(FuTable, verbose_name="赋分表", on_delete=models.DO_NOTHING, null=True, blank=True, )

    def __str__(self):
        return "%s的申请表"%self.sname

    class Meta:
        verbose_name = "申请表"
        verbose_name_plural = verbose_name


# 学术活动文件
class AcademicActivity(models.Model):
    applicationForm = models.ForeignKey(ApplicationForm, to_field='id', on_delete=models.CASCADE,
                                        related_name="student_academicActivityImage")
    name = models.CharField(verbose_name="文件名", max_length=100)
    academicActivityImage = models.ImageField(verbose_name="相关图片", upload_to="academicActivityImage")

    class Meta:
        verbose_name = "学术活动文件"
        verbose_name_plural = verbose_name


# 发表论文文件
class Publications(models.Model):
    applicationForm = models.ForeignKey(ApplicationForm, to_field='id', on_delete=models.CASCADE,
                                     related_name="student_publicationsImage")
    name = models.CharField(verbose_name="文件名", max_length=100)
    publicationsImage = models.ImageField(verbose_name="相关图片", upload_to="publicationsImage")

    class Meta:
        verbose_name = "发表论文文件"
        verbose_name_plural = verbose_name


# 参与项目文件
class ParticipateItems(models.Model):
    applicationForm = models.ForeignKey(ApplicationForm, to_field='id', on_delete=models.CASCADE,
                                         related_name="student_participateItemsImage")
    name = models.CharField(verbose_name="文件名", max_length=100)
    participateItemsImage = models.ImageField(verbose_name="相关图片", upload_to="participateItemsImage")

    class Meta:
        verbose_name = "参与项目文件"
        verbose_name_plural = verbose_name


# 科研项目
class ResearchProjects(models.Model):
    applicationForm = models.ForeignKey(ApplicationForm, to_field='id', on_delete=models.CASCADE,
                                         related_name="student_researchProjectsImage")
    name = models.CharField(verbose_name="文件名", max_length=100)
    researchProjectsImage = models.ImageField(verbose_name="相关图片", upload_to="researchProjectsImage")

    class Meta:
        verbose_name = "参与项目文件"
        verbose_name_plural = verbose_name


# 研究生创新项目
class InnovationProjects(models.Model):
    applicationForm = models.ForeignKey(ApplicationForm, to_field='id', on_delete=models.CASCADE,
                                           related_name="student_innovationProjectsImage")
    name = models.CharField(verbose_name="文件名", max_length=100)
    innovationProjectsImage = models.ImageField(verbose_name="相关图片", upload_to="innovationProjectsImage")

    class Meta:
        verbose_name = "研究生创新项目文件"
        verbose_name_plural = verbose_name


# 社会服务文件
class SocialWork(models.Model):
    applicationForm = models.ForeignKey(ApplicationForm, to_field='id', on_delete=models.CASCADE,
                                   related_name="student_socialWorkImage")
    name = models.CharField(verbose_name="文件名", max_length=100)
    socialWorkImage = models.ImageField(verbose_name="相关图片", upload_to="socialWorkImage")

    class Meta:
        verbose_name = "社会服务文件"
        verbose_name_plural = verbose_name


# 奖助评审会议
class Meeting(models.Model):
    title = models.CharField(verbose_name="申请会议名称", max_length=20, unique=True)
    student = models.ManyToManyField(Student, verbose_name="参与学生", blank=True, related_name="meeting_student")
    # jury = models.ManyToManyField(Jury, verbose_name="评委老师", blank=True)
    endTime = models.DateTimeField(verbose_name="申请结束时间")
    STATUS_CHOICE = [
        ('未开始', '未开始'),
        ('已开始', '已开始'),
        ('已结束', '已结束')
    ]
    # referTeacher = models.ManyToManyField(Jury, verbose_name="已提交评委", related_name="submit_teacher", blank=True)
    gradeStatus = models.CharField(verbose_name="评分状态", max_length=10, choices=STATUS_CHOICE, default='未开始')

    class Meta:
        verbose_name = "评审会议"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s'%self.title


# def save_model(self, request, obj, form, change):
#     if obj:
#         # Save the object
#         super().save_model(request, obj, form, change)
#         # Add the user instance to M2M field of the request.user (The admin User) who create the RegularUser
#     print(request, obj, form, change)

# @receiver(post_save, sender = Meeting)
# def addStudent(sender, instance, created, **kwargs ):
#     if created:
#         print(Meeting.objects.all())
#         # 获取当前时间前三年包括当前时间的学生, 例如: 2020 年那我就需要 2020 2019 2018 2017 的学生
#         import time
#         print("hello")
#         year = time.localtime().tm_year - 3
#         students = Student.objects.filter(startDate__gte="%s-8-1"%year)
#         for student in students:
#             instance.student.set(students)


# @receiver(post_save, sender = Meeting)
# def save_user_profile(sender, instance, **kwargs):
#     instance.student.save()


# 奖助等级
class GrantLevel(models.Model):
    title = models.CharField(verbose_name="名称", max_length=50)
    money = models.IntegerField(verbose_name="金额")
    text = models.TextField(verbose_name="说明", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "奖助学金等级"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s"%self.title


# 学生资格(本次会议中不符合要求的学生)
class Qualification(models.Model):
    meeting = models.ForeignKey(Meeting, verbose_name="相关会议", on_delete=models.CASCADE, related_name='meeting_for_student')
    sname = models.CharField(verbose_name="学生姓名", max_length=20)
    sno = models.CharField(verbose_name="学生学号", max_length=11)
    text = models.TextField(verbose_name="原因", max_length=200, default="无")

    def __str__(self):
        return "%s"%self.sname

    class Meta:
        verbose_name = "不符合资格学生"
        verbose_name_plural = "不符合资格学生"
        unique_together = ('meeting', 'sname')


# 不符合资格
class File1(models.Model):
    title = models.CharField(verbose_name="名称", max_length=20)
    file = models.FileField(verbose_name="文件", upload_to="testFile")


# 学生成绩
class StudentGrade(models.Model):
    sname = models.CharField(verbose_name='姓名', max_length=20)
    sno = models.CharField(verbose_name="学号", max_length=11)


# 申请成绩表
class ApplicationGrade(models.Model):
    teacher = models.ForeignKey(Jury, verbose_name="评委老师", on_delete=models.DO_NOTHING, related_name="jury_for_application_grade")
    applicationForm = models.ForeignKey(ApplicationForm, verbose_name="申请表", on_delete=models.CASCADE, related_name="applicationForm_grade")
    meeting = models.ForeignKey(Meeting, verbose_name="会议", on_delete=models.CASCADE, related_name="meeting_for_application_grade")
    title = models.CharField(verbose_name="赋分项", max_length=100)
    grade = models.SmallIntegerField(verbose_name="分数")
    chief_umpire = models.BooleanField(verbose_name="主审", default=False)

    class Meta:
        verbose_name = "申请表成绩"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "学生:%s, 评委:%s"%(self.applicationForm.sname, self.teacher.jname)


# class Grade(models.Model):
#     teacher = models.ForeignKey(Teacher, verbose_name="评委老师", on_delete=models.DO_NOTHING)
#     applicationForm = models.ForeignKey(ApplicationForm, verbose_name="申请表", on_delete=models.CASCADE, related_name="applicationForm_grade")
#     meeting = models.ForeignKey(Meeting, verbose_name="会议", on_delete=models.CASCADE)
#     chief_umpire = models.BooleanField(verbose_name="主审", default=False)
#     # 在这里输入四六级成绩就行,在计算时进行运算
#     # 保存运算后的结果
#     englishGrade = models.SmallIntegerField(verbose_name="四级/六级分数", null=True, blank=True)
#     baseGrade = models.SmallIntegerField(verbose_name="基本分", default=10)
#     #    学术活动分数
#     academicActivityGrade = models.SmallIntegerField(verbose_name="学术活动分数", null=True, blank=True)
#     #    发表论文
#     publicationsGrade = models.SmallIntegerField(verbose_name="发表论文分数", null=True, blank=True)
#     #    参与项目
#     participateItemsGrade = models.SmallIntegerField(verbose_name="参与项目分数", null=True, blank=True)
#     #    科研项目分数
#     researchProjectsGrade = models.SmallIntegerField(verbose_name="科研项目分数", null=True, blank=True)
#     # 研究生创新项目分数
#     innovationProjectsGrade = models.SmallIntegerField(verbose_name="研究生创新项目分数", null=True, blank=True)
#     # 社会服务分数
#     socialWorkGrade = models.SmallIntegerField(verbose_name="社会服务分数", null=True, blank=True)
#
#     class Meta:
#         verbose_name = "申请表成绩"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return "学生:%s, 评委:%s"%(self.applicationForm.sname, self.teacher.tname)


# 导师评分
class MentorGrade(models.Model):
    applicationForm = models.ForeignKey(ApplicationForm, verbose_name="申请表", on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, verbose_name="会议", on_delete=models.CASCADE)
    mentorGrade = models.SmallIntegerField(verbose_name="导师评分", null=True, blank=True)

    # def __str__(self):
    #     return "学生: %s"
    class Meta:
        verbose_name = "导师评分"
        verbose_name_plural = verbose_name


# 学生互评
class OtherStudentGrade(models.Model):
    applicationForm = models.ForeignKey(ApplicationForm, verbose_name="申请表", on_delete=models.CASCADE)
    otherGrade = models.SmallIntegerField(verbose_name="学生评分", null=True, blank=True)
    student = models.ForeignKey(Student, verbose_name="评分学生", on_delete=models.DO_NOTHING)
    meeting = models.ForeignKey(Meeting, verbose_name="会议", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "学生互评"
        verbose_name_plural = verbose_name


class Message(models.Model):
    from_user = models.ForeignKey(MyUser, verbose_name="发送者", on_delete=models.CASCADE, related_name="send_message")
    to_user = models.ForeignKey(MyUser, verbose_name="接收者", on_delete=models.CASCADE, related_name="have_message")
    text = models.TextField(verbose_name="信息内容", max_length=200)
    status = models.BooleanField(verbose_name="已读", default=False)
    send_time = models.DateTimeField(verbose_name="发送时间", auto_now_add=True)

    class Meta:
        verbose_name = "消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s给%s"%(self.from_user, self.to_user)


# 通知消息
class Notice(models.Model):
    title = models.CharField(verbose_name="标题", max_length=50)
    add_time = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    content = models.TextField(verbose_name="内容", max_length=500, blank=True, null=True)
    MESSAGE_TYPE = [
        ("公告通知", "公告通知"),
        ("评审通知", "评审通知"),
        ("结果通知", "结果通知"),
    ]
    message_type = models.CharField(verbose_name="公告类型", max_length=4, choices=MESSAGE_TYPE)
    show = models.BooleanField(verbose_name="是否展示")

    class Meta:
        verbose_name = "通知"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s"%self.title


class NoticeFile(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name="notice_files")
    file = models.FileField(verbose_name="文件", upload_to="notice", blank=True, null=True)

    class Meta:
        verbose_name = "公告文件"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.file).split("/")[1]


# 删除数据同时删除文件
@receiver(pre_delete, sender=AcademicActivity) #sender=你要删除或修改文件字段所在的类**
def delete_academicActivityImage(instance, **kwargs):       #函数名随意
    instance.academicActivityImage.delete(False) #file是保存文件或图片的字段名**


@receiver(pre_delete, sender=Publications)  # sender=你要删除或修改文件字段所在的类**
def delete_publicationsImage(instance, **kwargs):  # 函数名随意
    instance.publicationsImage.delete(False)  # file是保存文件或图片的字段名**


@receiver(pre_delete, sender=ParticipateItems)  # sender=你要删除或修改文件字段所在的类**
def delete_participateItems (instance, **kwargs):  # 函数名随意
    instance.participateItemsImage.delete(False)  # file是保存文件或图片的字段名**


@receiver(pre_delete, sender=InnovationProjects)  # sender=你要删除或修改文件字段所在的类**
def delete_innovationProjects (instance, **kwargs):  # 函数名随意
    instance.innovationProjectsImage.delete(False)  # file是保存文件或图片的字段名**


@receiver(pre_delete, sender=ResearchProjects)  # sender=你要删除或修改文件字段所在的类**
def delete_researchProjects (instance, **kwargs):  # 函数名随意
    instance.researchProjectsImage.delete(False)  # file是保存文件或图片的字段名**


@receiver(pre_delete, sender=SocialWork)  # sender=你要删除或修改文件字段所在的类**
def delete_socialWork (instance, **kwargs):  # 函数名随意
    instance.socialWorkImage.delete(False)  # file是保存文件或图片的字段名**