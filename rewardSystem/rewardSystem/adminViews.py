from xadmin.views import CommAdminView
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.core.paginator import Paginator
from dataManagement.models import Meeting, File1, Qualification, FuTable
import time, hashlib, os, struct, xlrd


class MeetingManage(CommAdminView):
    def get(self, request):
        context = super().get_context()
        title = "会议设置"
        context["breadcrumbs"].append({'url': '/cwyadmin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面
        # 获取会议列表
        meeting_list = Meeting.objects.all().order_by('id')
        paginator = Paginator(meeting_list, 30)
        page_num = request.GET.get('page', 1)
        page_of_meetings = paginator.get_page(page_num)
        context["page_of_meetings"] = page_of_meetings

        return render(request, 'meetingManage.html', context)

    # def get_url(self, app_name, stream_name):
    #     t = time.time() + 172800
    #     keytime = str(int(t))
    #     hashstring = "/" + app_name + "/" + stream_name + "-" + keytime + "-0-0-" + app_name + "alipush"
    #     m = hashlib.md5()
    #     m.update(hashstring.encode("utf8"))
    #     mm = m.hexdigest()
    #     print(mm)
    #     push = "rtmp://" + app_name + "alipush.v.myalicdn.com/" + app_name + "/" + stream_name + "?auth_key=" + keytime + "-0-0-" + mm
    #     return push


class ImportStudent(CommAdminView):
    def get(self, request):
        context = super().get_context()
        title = "不符合资格学生"
        context["breadcrumbs"].append({'url': '/cwyadmin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面
        # 获取不符合资格学生
        meeting_id = request.GET.get('id')
        meeting = get_object_or_404(Meeting, pk=meeting_id)
        meeting_for_student = meeting.meeting_for_student.all()
        context['meeting_id'] = meeting_id
        context['meeting'] = meeting
        context['meeting_for_student'] = meeting_for_student

        return render(request, template_name="importStudent.html", context=context)

    def post(self, request):
        form_url = request.META.get('HTTP_REFERER', )
        file = request.FILES.get('file')
        id = request.POST.get('pk')
        meeting_obj = get_object_or_404(Meeting, pk=id)
        rexcel = xlrd.open_workbook(filename=None, file_contents=file.read())
        # 获取表格
        sheet = rexcel.sheet_by_index(0)
        row = 1
        while True:
            try:
                rows = sheet.row_values(row)
                objs = Qualification.objects.filter(meeting=meeting_obj, sno=rows[1])
                if not objs:
                    Qualification.objects.create(meeting=meeting_obj, sname=rows[0], sno=rows[1], text=rows[2])
                row += 1
            except IndexError:
                break
        return redirect(form_url)


class Download_student_xls(CommAdminView):

    def get(self, request):
        field = request.GET.get('q')
        if field == "学生信息表":
            file = open(os.getcwd() + '/media/studentMuBan/学生信息模板.xlsx', 'rb')
            file_name = "学生信息表模板"
        elif field == "老师信息表":
            file = open(os.getcwd() + '/media/studentMuBan/老师信息模板.xlsx', 'rb')
            file_name = "老师信息模板"
        else:
            file = open(os.getcwd()+'/media/studentMuBan/student.xlsx', 'rb')
            file_name = "student"
        response = HttpResponse(file)
        response['Content_Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s.xlsx"'%file_name.encode('utf-8').decode('ISO-8859-1')
        # response['Content-Disposition'] = 'attachment;filename="student.xlsx"'

        return response


class AssignTables(CommAdminView):
    def get(self, request):

        context = super().get_context()
        title = "分配赋分表"
        context["breadcrumbs"].append({'url': '/cwyadmin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面
        # 获取 会议列表用来为 select 展示
        meeting_list = Meeting.objects.all()
        # 获取赋分表(赋分表是为学生的申请表关联的)
        fuTable_list = FuTable.objects.all()
        context["meeting_list"] = meeting_list
        context["fuTable_list"] = fuTable_list
        return render(request, template_name="assignTables.html", context=context)

    def post(self, request):
        form_url = request.META.get('HTTP_REFERER', )
        meeting_id = request.POST.get('meeting')
        # 赋分表编号
        futable = request.POST.get("futable")
        # 学号
        studentsno = request.POST.get("studentsno")
        # 姓名
        studentsname = request.POST.get("studentsname")
        print(futable, meeting_id, studentsname, studentsno)
        if meeting_id and futable:
            meeting = get_object_or_404(Meeting, id=meeting_id)
            if studentsno:
                # 会议中的学生的申请表
                applicationForm_obj = meeting.meeting_for_applicationform.get(sno=studentsno)
                applicationForm_obj.fuTable = get_object_or_404(FuTable, pk=futable)
                applicationForm_obj.save()
            elif studentsname:
                applicationForm_obj = meeting.meeting_for_applicationform.all()
                applicationForm_obj.fuTable = get_object_or_404(FuTable, pk=futable)
                applicationForm_obj.save()
            else:
                applicationForm_objs = meeting.meeting_for_applicationform.all()
                for applicationForm_obj in applicationForm_objs:
                    applicationForm_obj.fuTable = get_object_or_404(FuTable, pk=futable)
                    applicationForm_obj.save()

        return redirect(form_url)
