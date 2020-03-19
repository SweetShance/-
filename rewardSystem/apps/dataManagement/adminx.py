import xadmin, xlrd, os
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from .models import Student, Teacher, ApplicationForm, Meeting, FuTable, AssignItem, GrantLevel, AcademicActivity, Publications,\
                    ParticipateItems, ResearchProjects, InnovationProjects, SocialWork, Qualification


# 学生
class StudentAdmin:
    list_display = ['sno', 'sname', 'sex', 'startDate', 'tutor', 'registerStatus', 'status']
    list_filter = ['startDate', 'tutor', 'registerStatus', 'status', 'sex', 'admissionstatus']
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
    list_display = ['tno', 'tname', 'sex', 'register_status']
    list_filter = ['sex', 'register_status']
    search_fields = ['tno', 'tname']
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


# 会议
class MeetingAdmin:
    list_display = ['title', 'endTime', 'gradeStatus']
    list_filter = ['endTime', 'title']
    search_fields = ['title']
    list_editable = ["endTime", "gradeStatus"]
    fields = ('title', 'student' ,'jury', 'endTime', 'gradeStatus')


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
    list_display = ['title', 'money']


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
    list_display = ['sno', 'sname', 'upload_time', 'otherstatus', 'activity', 'grant', 'jury']
    list_filter = ['meeting__title', 'otherstatus', 'activity', 'grant', 'jury']
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


