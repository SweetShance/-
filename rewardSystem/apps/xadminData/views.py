from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import json, random, xlwt, os
from io import BytesIO
from dataManagement.models import Student, Meeting, Qualification, ApplicationForm, Jury, StudentGrade
from MyUser.models import MyUser


# Create your views here.
class MeetingDeleteStudent(View):
    def get(self, request):
        pass

    def post(self, request):
        student_list = json.loads(request.POST.get("student_id"))
        meeting_id = request.POST.get("meeting_id")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        try:
            for student_id in student_list:
                student_obj = get_object_or_404(Student, pk=student_id)
                meeting_obj.student.remove(student_obj)
        except ObjectDoesNotExist:
            return JsonResponse({"status": "失败"})
        return JsonResponse({"status": "成功"})


# 添加单个学生
class MeetingAddStudentList(View):
    def get(self, request):
        pass

    def post(self, request):
        _q_ = request.POST.get("q")
        meeting_id = request.POST.get("meeting_id")
        student_list = []
        context = {}
        if _q_:
            students = Student.objects.filter(Q(sname__contains=_q_) | Q(sno__contains=_q_))
            # context["students"] = students
            for student in students:
                status = get_object_or_404(Meeting, pk=meeting_id).student.filter(sno=student.sno)
                if status:
                    student_list.append([student, "是"])
                else:
                    student_list.append([student, "否"])
            context["student_list"] = student_list
            context["meeting_id"] = meeting_id

        return render(request, template_name="xadminData/addStudentList.html", context=context)


class MeetingAddStudent(View):
    def post(self, request):
        print("hello")
        meeting_id = request.POST.get("meeting_id")
        student_id_list = json.loads(request.POST.get('student_id'))
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)

        try:
            for student_id in student_id_list:
                student_obj = get_object_or_404(Student, pk=student_id)
                if not meeting_obj.student.filter(sno=student_obj.sno):
                    meeting_obj.student.add(student_obj)
        except ObjectDoesNotExist:
            return JsonResponse({"status": "失败"})

        return JsonResponse({"status": "成功"})


# 分配评委
"""
思路: 当前会议学生(申请表)关联评委, 规范是评委不能是此学生导师,
每个导师关联几个学生
"""


class MeetingImportAddStudent(View):

    def post(self, request):
        meeting_id = request.POST.get("meeting_id")
        sname = request.POST.get("name")
        sno = request.POST.get("sno")
        text = request.POST.get("text")
        try:
            meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
            stu_obj_list = Qualification.objects.filter(meeting=meeting_obj, sno=sno)
            if stu_obj_list:
                return JsonResponse({"status": "该学生已存在"})
            else:
                Qualification.objects.create(meeting=meeting_obj, sname=sname, sno=sno, text=text)
                return JsonResponse({"status": "成功"})
        except Exception:
            return JsonResponse({"status": "失败"})


class MeetingImportDeleteStudent(View):

    def post(self, request):
        meeting_id = request.POST.get("meeting_id")
        student_id_list = request.POST.get("checkedArr")
        try:
            meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
            for student_id in json.loads(student_id_list):
                Qualification.objects.get(meeting=meeting_obj, pk=student_id).delete()
            return JsonResponse({"status": "成功"})
        except Exception:
            return JsonResponse({"status": "失败"})


class MeetingImportChangeStudent(View):
    def post(self, request):
        meeting_id = request.POST.get('meeting_id')
        sno = request.POST.get("sno")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        # Qualification.objects.get(Meeting=meeting_obj, sno=sno)
        qualification_student_obj = get_object_or_404(Qualification, meeting=meeting_obj, sno=sno)
        context = {
            "qualification_student_obj": qualification_student_obj
        }
        return render(request, template_name="xadminData/importStudentChange.html", context=context)


class MeetingImportChangeStudentSave(View):
    def post(self, request):
        meeting_id = request.POST.get('meeting_id')
        student_id = request.POST.get("student_id")
        sno = request.POST.get("sno")
        sname = request.POST.get("sname")
        text = request.POST.get("text")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        # Qualification.objects.get(Meeting=meeting_obj, sno=sno)
        qualification_student_obj = get_object_or_404(Qualification, meeting=meeting_obj, pk=student_id)
        qualification_student_obj.sname = sname
        qualification_student_obj.sno = sno
        qualification_student_obj.text = text
        qualification_student_obj.save()
        return JsonResponse({"status": "成功"})

    def get(self, request):
        return HttpResponse("hello")


# 分配评委
class AllotJurySave(View):
    def post(self, request):
        # ["申请表id:评委id"]
        applicationform_list_jury = request.POST.get("applicationform_list_jury")
        try:
            for applicationform_jury in json.loads(applicationform_list_jury):
                applicationform_id = applicationform_jury.split(":")[0]
                jury_id = applicationform_jury.split(":")[1]
                applicationform_obj = get_object_or_404(ApplicationForm, pk=applicationform_id)
                jury_obj = get_object_or_404(Jury, pk=jury_id)
                applicationform_obj.jury = jury_obj
                applicationform_obj.save()
        except Exception:
            return JsonResponse({"status": "失败"})

        return JsonResponse({"status": "成功"})


# 一键添加近三年的学生
class MeetingToAddAllStudent(View):
    def post(self, request):
        # 获取meeting_id
        meeting_id = request.POST.get("meeting_id")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        import time
        # 获取学生
        year = time.localtime().tm_year - 2
        students = Student.objects.filter(startDate__gte="%s-8-1"%year)
        meeting_obj.student.set(students)
        return JsonResponse({"status": "成功"})


# 评委分配账户
class MeetingJuryAllotAccount(View):
    def post(self, request):
        juryIdList = request.POST.get("juryId")
        for juryId in json.loads(juryIdList):
            jury_obj = get_object_or_404(Jury, pk=juryId)
            # 没有创建用户
            if not jury_obj.user_id:
                # 随机用户名
                tag = True
                while tag:
                    username = ""
                    for i in range(0, 9):
                        if i == 0:
                            username += str(random.randint(1, 10))
                        else:
                            username += str(random.randint(0, 10))
                    this_user = MyUser.objects.filter(username=username.strip())
                    if not this_user:
                        tag = False
                # # 随机密码
                password = ""
                for i in range(0, 6):
                    num = random.randint(0, 9)
                    alf = chr(random.randint(97, 122))
                    s = str(random.choice([num, alf]))
                    password += s
                    # 创建用户
                user_obj = MyUser.objects.create_user(username=username.strip(), password=password.strip(), name=jury_obj.jname, identity="评委")
                jury_obj.jno = username
                jury_obj.password = password
                jury_obj.user_id = user_obj.id
                jury_obj.save()

        return JsonResponse({"status": "成功"})


# 导出账户
class ExportAccount(View):
    def get(self, requets):
        meeting_id = requets.GET.get("meeting_id")
        # 创建工作表
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = response['Content-Disposition'] = 'attachment;filename="%s".xls' % "评委用户".encode('utf-8').decode(
            'ISO-8859-1')
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet('sheet1')
        # 写入表头
        worksheet.write(0, 0, "姓名")
        worksheet.write(0, 1, "用户名")
        worksheet.write(0, 2, "密码")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        meeting_jury_list = meeting_obj.jury.all()
        execel_row = 1
        # 写表头
        for jury in meeting_jury_list:
            worksheet.write(execel_row, 0, jury.jname)
            worksheet.write(execel_row, 1, jury.jno)
            worksheet.write(execel_row, 2, jury.password)
            execel_row += 1
        # 设置HTTPResponse的类型
        """导出excel表"""
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response


# 学生成绩
# 下载学生成绩模板
class Download_student_Grade(View):
    def get(self, request):
        file = open(os.getcwd()+'/media/studentMuBan/学生成绩模板.xlsx', 'rb')
        file_name = "学生成绩模板"
        response = HttpResponse(file)
        response['Content_Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s.xlsx"'%file_name.encode('utf-8').decode('ISO-8859-1')
        # response['Content-Disposition'] = 'attachment;filename="student.xlsx"'

        return response


# 添加成绩
class AddStudentGrade(View):
    def post(self, request):
        sno = request.POST.get('sno')
        sname = request.POST.get('sname')
        grade1 = request.POST.get('number1')
        grade2 = request.POST.get('number2')
        meeting_id = request.POST.get('meeting_id')
        print("hello")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        student_Grade_objs = StudentGrade.objects.filter(sno=sno)
        if student_Grade_objs:
            return JsonResponse({"status": "该学生已存在"})
        else:
            StudentGrade.objects.create(meeting=meeting_obj, sno=sno, sname=sname, grade1=grade1, grade2=grade2)
            return JsonResponse({"status": "添加成功"})


# 修改成绩
class MeetingChangeStudentGrade(View):
    def post(self, request):
        meeting_id = request.POST.get("meeting_id")
        sno = request.POST.get("sno")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        studentGradeObjs = meeting_obj.meeting_student_grade.filter(sno=sno)
        if studentGradeObjs:
            context = {
                "studentGradeObj": studentGradeObjs[0]
            }
        return render(request, template_name="xadminData/ChangStudentGrade.html", context=context)


# 修改成绩保存
class MeetingChangStudentGradeSave(View):
    def post(self, request):
        meeting_id = request.POST.get("meeting_id")
        sno = request.POST.get("sno")
        sname = request.POST.get("sname")
        graded1 = request.POST.get("number1")
        graded2 = request.POST.get("number2")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        studentGradeObjs = meeting_obj.meeting_student_grade.filter(sno=sno)
        if studentGradeObjs:
            studentGradeObj = studentGradeObjs[0]
            studentGradeObj.sno = sno
            studentGradeObj.sname = sname
            studentGradeObj.grade1 = graded1
            studentGradeObj.grade2 = graded2
            studentGradeObj.save()
            return JsonResponse({'status': "成功"})
        else:
            return JsonResponse({"status": "该学生不存在"})


class MeetingChangStudentGradeDelete(View):
    def post(self, request):
        meeting_id = request.POST.get("meeting_id")
        sno_list = request.POST.get("checkedArr")
        no_list = []
        data = {}
        for sno in json.loads(sno_list):
            meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
            studentGradeObjs = meeting_obj.meeting_student_grade.filter(sno=sno)
            if studentGradeObjs:
                studentGradeObj = studentGradeObjs[0]
                studentGradeObj.delete()
                data["status"] = "成功"
            else:
                no_list.append(sno)
        if no_list:
            data["status"] = str(no_list) + "不存在"
            return JsonResponse(data)
        return JsonResponse(data)

