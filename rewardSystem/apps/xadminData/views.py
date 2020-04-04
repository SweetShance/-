from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import json
from dataManagement.models import Student, Meeting, Qualification, ApplicationForm, Teacher


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
        print(meeting_id, student_id_list)
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
                print("hello")
                Qualification.objects.create(meeting=meeting_obj, sname=sname, sno=sno, text=text)
                return JsonResponse({"status": "成功"})
        except Exception:
            return JsonResponse({"status": "失败"})


class MeetingImportDeleteStudent(View):

    def post(self, request):
        print(request.POST)
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
                jury_obj = get_object_or_404(Teacher, pk=jury_id)
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