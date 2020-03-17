from django.db import models
from django.utils import timezone
from django.forms import fields
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
    status = models.BooleanField(verbose_name="申请资格", default=True)

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
    fuTable = models.ForeignKey(FuTable, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="赋分项", max_length=50)
    grade = models.IntegerField(verbose_name="分数")
    scoring = models.TextField(verbose_name="赋分标准", max_length=300)
    state = models.TextField(verbose_name="说明", max_length=300)

    class Meta:
        verbose_name = "赋分项列表"
        verbose_name_plural = verbose_name


# 申请表
class ApplicationForm(models.Model):
    student = models.ForeignKey(Student, verbose_name="学生", on_delete=models.CASCADE, related_name="student_applicationform")
    sno = models.CharField(max_length=11, verbose_name="学生学号")
    sname = models.CharField(max_length=20, verbose_name="学生姓名")
    presentation = models.TextField(max_length=500, verbose_name="学生简介")
    baseGrade = models.SmallIntegerField(verbose_name="基本分", default=10)
    ETC_CHOICe = [
        ('四级', '四级'),
        ('六级', '六级')
    ]

    englishChoice = models.CharField(max_length=2, verbose_name="四级/六级", choices=ETC_CHOICe, default="四级")
    etcImage = models.ImageField(verbose_name="四级/六级图片", upload_to='ETCImage', blank=True)
    englishGrade = models.IntegerField(verbose_name="四级/六级分数")
    # 学术活动
    academicActivityText = models.CharField(verbose_name="参与学术活动介绍", max_length=500)
    academicActivityGrade = models.SmallIntegerField(verbose_name="学术活动分数", null=True, blank=True)
    # 发表论文
    publicationsText = models.CharField(verbose_name="发表论文介绍", max_length=500)
    publicationsGrade = models.SmallIntegerField(verbose_name="发表论文分数", null=True, blank=True)
    # 参与项目
    participateItemsText = models.CharField(verbose_name="参与项目介绍", max_length=500)
    participateItemsGrade = models.SmallIntegerField(verbose_name="参与项目分数", null=True, blank=True)
    # 科研项目
    researchProjectsText = models.CharField(verbose_name="科研项目介绍", max_length=500)
    researchProjectsGrade = models.SmallIntegerField(verbose_name="科研项目分数", null=True, blank=True)
    # 研究生创新项目
    innovationProjectsText = models.CharField(verbose_name="研究生创新项目介绍", max_length=500)
    innovationProjectsGrade = models.SmallIntegerField(verbose_name="研究生创新项目分数", null=True, blank=True)
    # 社会服务
    socialWorkText = models.CharField(verbose_name="社会服务介绍", max_length=500)
    socialWorkGrade = models.SmallIntegerField(verbose_name="社会服务分数", null=True, blank=True)
    mentorGrade = models.SmallIntegerField(verbose_name="导师评分", null=True, blank=True)
    otherGrade = models.SmallIntegerField(verbose_name="学生评分", null=True, blank=True)
    otherstatus = models.BooleanField(verbose_name="学生互评状态")
    judgesGrade = models.SmallIntegerField(verbose_name="评委赋分", null=True, blank=True)
    upload_time = models.DateTimeField(verbose_name="提交时间", auto_now_add=True)
    evaluate = models.TextField(verbose_name="说明", max_length=200)
    # 等级
    grant = models.ForeignKey('GrantLevel', verbose_name="等级", on_delete=models.CASCADE, null=True)
    activity = models.BooleanField(verbose_name="是否通过审核", default=False)
    jury = models.ForeignKey(Teacher, verbose_name="评委", on_delete=models.DO_NOTHING, null=True, blank=True)
    # 会议
    meeting = models.ForeignKey('Meeting', verbose_name="所属会议", on_delete=models.CASCADE, related_name="meeting_for_applicationform")
    # 赋分表
    fuTable = models.ForeignKey(FuTable, verbose_name="赋分表", on_delete=models.DO_NOTHING, null=True, blank=True, )

    def __str__(self):
        return "%s的赋分表"%self.sname

    class Meta:
        verbose_name = "申请表"
        verbose_name_plural = verbose_name


# 学术活动文件
class AcademicActivity(models.Model):
    applicationForm = models.ForeignKey(ApplicationForm, to_field='id', on_delete=models.CASCADE,
                                        related_name="student_academicActivityImage")
    academicActivityImage = models.ImageField(verbose_name="相关图片", upload_to="academicActivityImage")

    class Meta:
        verbose_name = "学术活动文件"
        verbose_name_plural = verbose_name


# 发表论文文件
class Publications(models.Model):
    publications = models.ForeignKey(ApplicationForm, to_field='id', on_delete=models.CASCADE,
                                     related_name="student_publicationsImage")
    publicationsImage = models.ImageField(verbose_name="相关图片", upload_to="publicationsImage")

    class Meta:
        verbose_name = "发表论文文件"
        verbose_name_plural = verbose_name


# 参与项目文件
class ParticipateItems(models.Model):
    participateItems = models.ForeignKey(ApplicationForm, to_field='id', on_delete=models.CASCADE,
                                         related_name="student_participateItemsImage")
    publicationsImage = models.ImageField(verbose_name="相关图片", upload_to="participateItemsImage")

    class Meta:
        verbose_name = "参与项目文件"
        verbose_name_plural = verbose_name


# 科研项目
class ResearchProjects(models.Model):
    researchProjects = models.ForeignKey(ApplicationForm, to_field='id', on_delete=models.CASCADE,
                                         related_name="student_researchProjectsImage")
    researchProjectsImage = models.ImageField(verbose_name="相关图片", upload_to="researchProjectsImage")

    class Meta:
        verbose_name = "参与项目文件"
        verbose_name_plural = verbose_name


# 研究生创新项目
class InnovationProjects(models.Model):
    innovationProjects = models.ForeignKey(ApplicationForm, to_field='id', on_delete=models.CASCADE,
                                           related_name="student_innovationProjectsImage")
    innovationProjectsImage = models.ImageField(verbose_name="相关图片", upload_to="innovationProjectsImage")

    class Meta:
        verbose_name = "研究生创新项目文件"
        verbose_name_plural = verbose_name


# 社会服务文件
class SocialWork(models.Model):
    socialWork = models.ForeignKey(ApplicationForm, to_field='id', on_delete=models.CASCADE,
                                   related_name="student_socialWorkImage")
    socialWorkImage = models.ImageField(verbose_name="相关图片", upload_to="socialWorkImage")

    class Meta:
        verbose_name = "社会服务文件"
        verbose_name_plural = verbose_name


# 奖助评审会议
class Meeting(models.Model):
    title = models.CharField(verbose_name="申请会议名称", max_length=20, unique=True)
    student = models.ManyToManyField(Student, verbose_name="参与学生", blank=True)
    jury = models.ManyToManyField(Teacher, verbose_name="评委老师", blank=True)
    endTime = models.DateTimeField(verbose_name="申请结束时间")
    STATUS_CHOICE = [
        ('未开始', '未开始'),
        ('已开始', '已开始'),
        ('已结束', '已结束')
    ]
    gradeStatus = models.CharField(verbose_name="评分状态", max_length=10, choices=STATUS_CHOICE, default='未开始')

    class Meta:
        verbose_name = "评审会议"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s'%self.title


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



