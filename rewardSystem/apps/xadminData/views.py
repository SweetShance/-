from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import json
from dataManagement.models import Student, Meeting


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

        return render(request, template_name="addStudentList.html", context=context)

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


