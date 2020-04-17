import xadmin, xlrd, os
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from .models import Student, Teacher, ApplicationForm, Meeting, FuTable, AssignItem, GrantLevel, AcademicActivity, Publications,\
                    ParticipateItems, ResearchProjects, InnovationProjects, SocialWork, Qualification, Message, ApplicationGrade,\
                    Notice, NoticeFile, Jury, StudentGrade, MentorGrade, OtherStudentGrade


# 学生
class StudentAdmin:
    list_display = ['sno', 'sname', 'sex', 'startDate', 'tutor', 'registerStatus']
    list_filter = ['startDate', 'tutor', 'registerStatus', 'sex', 'admissionstatus']
    search_fields = ['sno', 'sname']
    import_excel = True
    download_excel_templates = True

    def post(self, request, *args, **kwargs):

        if 'excel' in request.FILES:
            file = request.FILES.get('excel')
            wb = xlrd.open_workbook(filename=None, file_contents=file.read())
            sheet = wb.sheet_by_index(0)
            row = 1
            while True:
                try:
                    row_content = sheet.row_values(row)
                    sno = row_content[0]
                    sname = row_content[1]
                    sex = row_content[2]
                    startDate = xlrd.xldate_as_datetime(row_content[3], 0).strftime('%Y-%m-%d')
                    stu_obj = Student.objects.filter(sno=sno)
                    if stu_obj:
                        row += 1
                        continue
                    tutor = get_object_or_404(Teacher, tno=row_content[4])
                    admissionstatus = row_content[6]
                    Student.objects.create(sno=sno, sname=sname, sex=sex, startDate=startDate, tutor=tutor, admissionstatus=admissionstatus)
                    row += 1
                except IndexError:
                    break
        return super(StudentAdmin, self).post(request, *args, **kwargs)


xadmin.site.register(Student, StudentAdmin)


# 老师
class TeacherAdmin:
    list_display = ['tno', 'tname', 'sex', 'register_status', 'password']
    list_filter = ['sex', 'register_status']
    search_fields = ['tno', 'tname']
    readonly_fields = ['password']
    import_excel = True
    download_excel_templates = True
    allocated_account = True

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            file = request.FILES.get('excel')
            wb = xlrd.open_workbook(filename=None, file_contents=file.read())
            sheet = wb.sheet_by_index(0)
            row = 1
            while True:
                try:
                    row_content = sheet.row_values(row)
                    tno = row_content[0]
                    tname = row_content[1]
                    sex = row_content[2]
                    teacher_obj = Teacher.objects.filter(tno=tno)
                    if teacher_obj:
                        row += 1
                        continue
                    Teacher.objects.create(tno=tno, tname=tname, sex=sex)
                    row += 1
                except IndexError:
                    break
        return super(TeacherAdmin, self).post(request, *args, **kwargs)


xadmin.site.register(Teacher, TeacherAdmin)


# 评委
class JuryAdmin:
    model = Jury
    extra = 1
    style = 'table'
    list_display = ["jno", "jname", "password"]
    list_filter = ["meeting__title"]
    readonly_fields = ['jno', 'password', 'user_id']
    fields = ("jno", "jname", "password")


xadmin.site.register(Jury, JuryAdmin)


# 会议
class MeetingAdmin:
    list_display = ['title', 'endTime', 'gradeStatus']
    list_filter = ['endTime', 'title']
    search_fields = ['title']
    list_editable = ["endTime", "gradeStatus"]
    # fields = ('title', 'student' ,'jury', 'endTime', 'gradeStatus')
    fields = ('title', 'endTime', 'gradeStatus')
    # readonly_fields = ['referTeacher']
    inlines = [JuryAdmin]



xadmin.site.register(Meeting, MeetingAdmin)


# 赋分项(关联数据)
class AssignItemTabularInline:
    model = AssignItem # 致命类
    extra = 1
    style = 'table'


# 赋分表
class FuTableAdmin:
    list_display = ['title']
    inlines = [AssignItemTabularInline]


xadmin.site.register(FuTable, FuTableAdmin)


# 奖助等级
class GrantLevelAdmin:
    list_display = ['sort', 'title', 'money']


xadmin.site.register(GrantLevel, GrantLevelAdmin)


# 学术活动
class AcademicActivityInline:
    model = AcademicActivity
    extra = 1
    style = 'table'


# 发表论文
class PublicationsInline:
    model = Publications
    extra = 1
    style = 'table'


# 参与项目
class ParticipateItemsInline:
    model = ParticipateItems
    extra = 1
    style = 'table'


# 科研项目
class ResearchProjectsInline:
    model = ResearchProjects
    extra = 1
    style = 'table'


# 研究生创新项目项目
class InnovationProjectsInline:
    model = InnovationProjects
    extra = 1
    style = 'table'


# 社会服务文件
class SocialWorkInline:
    model = SocialWork
    extra = 1
    style = 'table'


# 申请表
class ApplicationFormAdmin:
    list_display = ['sno', 'sname', 'upload_time', 'otherstatus', "tootherstatus", 'activity', 'jury']
    list_filter = ['meeting__title', 'otherstatus', 'activity', 'jury', "tootherstatus"]
    inlines = [AcademicActivityInline, PublicationsInline, ParticipateItemsInline, ResearchProjectsInline, \
               InnovationProjectsInline, SocialWorkInline]
    search_fields = ['sno', 'sname']


xadmin.site.register(ApplicationForm, ApplicationFormAdmin)


# 不符合资格学生
class QualificationAdmin:
    list_display = ['meeting', 'sno', 'sname']
    list_filter = ['meeting__title']
    search_fields = ['sno', 'sname']


xadmin.site.register(Qualification, QualificationAdmin)


# 申请表成绩
class GradeAdmin:
    list_display = ["applicationForm", "teacher", "meeting", "title", "grade", "chief_umpire"]
    list_filter = ["teacher__jname", "meeting__title", "applicationForm__sname"]


xadmin.site.register(ApplicationGrade, GradeAdmin)


# 学生考试成绩
class StudentGradeAdmin:
    list_display = ["meeting", "sno", "sname", "grade1", "grade2"]
    list_filter = ["meeting__title"]


xadmin.site.register(StudentGrade, StudentGradeAdmin)


# 导师评分
class MentorGradeAdmin:
    list_display = ["applicationForm", "meeting", "mentorGrade"]
    list_filter = ["meeting__title"]
    # search_fields = ["applicationForm"]


xadmin.site.register(MentorGrade, MentorGradeAdmin)


# 学生互评
class OtherStudentGradeAdmin:
    list_display = ["applicationForm", "student", "meeting", "otherGrade"]
    list_filter = ["meeting"]


xadmin.site.register(OtherStudentGrade, OtherStudentGradeAdmin)


# 消息
class MessageAdmin:
    list_display = ["get_from_name", "get_to_name", "send_time", "status"]
    list_filter = ["from_user__name", "to_user__name", "status"]

    def get_from_name(self, obj):
        return obj.from_user.name

    get_from_name.short_description = '发送者'

    def get_to_name(self, obj):
        return obj.to_user.name
    get_to_name.short_description = '接收者'


xadmin.site.register(Message, MessageAdmin)

# 公告文件
class NoticeFileInline:
    model = NoticeFile # 致命类
    extra = 1
    style = 'table'


# 公告
class NoticeAdmin:
    list_display = ["title", "message_type", "add_time", "show"]
    list_filter = ["show", "message_type", ]
    inlines = [NoticeFileInline]


xadmin.site.register(Notice, NoticeAdmin)
