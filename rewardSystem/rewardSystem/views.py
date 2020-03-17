from django.shortcuts import render, get_object_or_404
from django.views import View
from dataManagement.models import Meeting

# Create your views here.


# 在分配赋分表中用 $.load 展示会议中的学生
class MeetingStudent(View):
    def post(self, request):
        meeting_id = request.POST.get('pk')
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        meetingStudentsApplicationForm = []
        if "studentname" in request.POST:
            if "studentsno" in request.POST:
                meetingStudents = meeting_obj.student.filter(sno = request.POST.get("studentsno"))

            else:
                meetingStudents = meeting_obj.student.filter(sname=request.POST.get("studentname"))
        else:
            meetingStudents = meeting_obj.student.all()

        for meetingStudent in meetingStudents:
            if meetingStudent.student_applicationform.filter(meeting=meeting_obj):
                meetingStudentsApplicationForm.append(meetingStudent.student_applicationform.filter(meeting=meeting_obj)[0])

        context = {
            "meetingStudentsApplicationForm": meetingStudentsApplicationForm
        }
        return render(request, template_name='meeting_for_student.html', context=context)


