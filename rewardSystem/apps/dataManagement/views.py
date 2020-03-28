from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.views import View
from MyUser.models import MyUser
from dataManagement.models import Student, Teacher, Meeting, ApplicationForm, AcademicActivity, Publications,\
    ParticipateItems, ResearchProjects, InnovationProjects, SocialWork


# Create your views here.
class Index(View):
    def get(self, request):
        return render(request, template_name="dataManagement/index.html", context={})


class MyInfo(View):
    def get(self, request):
        # 返回 用户信息, 姓名, 电话, 邮箱, 身份只读,
        # 返回 学生信息, 性别, 入学年份(只读), 导师(只读), 四级次数,六级次数(只读), 入学身份(只读)
        user_obj = get_object_or_404(MyUser, pk=request.user.id)
        user_info = []
        # 获取老师或学生
        if request.user.identity == "学生":
            if Student.objects.filter(sno=request.user.username):
                user_info = get_object_or_404(Student, sno=request.user.username)
        elif request.user.identity == "老师":
            if Teacher.objects.filter(tno=request.user.username):
                user_info = get_object_or_404(Teacher, tno=request.user.username)
        content = {
            "user_obj": user_obj,
            "user_info": user_info
        }

        return render(request, template_name="dataManagement/MyInfo.html", context=content)

    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        sex = request.POST.get("sex")
        identity = request.POST.get("identity")
        user_obj = get_object_or_404(MyUser, pk=request.user.id)
        user_obj.name = name
        user_obj.email = email
        user_obj.phone = phone
        user_obj.save()
        if identity == "老师":
            if Teacher.objects.filter(tno=request.user.username):
                user_info = get_object_or_404(Teacher, tno=request.user.username)
                user_info.sex = sex
                user_info.save()
                return JsonResponse({"status": "成功"})
            else:
                return JsonResponse({"status": "学生不存在"})
        elif identity == "学生":
            if Student.objects.filter(sno=request.user.username):
                user_info = get_object_or_404(Student, sno=request.user.username)
                user_info.sex = sex
                user_info.save()
                return JsonResponse({"status": "成功"})
            else:
                return JsonResponse({"status": "老师不存在"})


class SetPassword(View):
    def get(self, request):

        return render(request, template_name="dataManagement/setPassword.html", context={})

    def post(self, request):
        oldPassword = request.POST.get("OldPassword")
        newPassword = request.POST.get("NewPassword")
        user = auth.authenticate(username=request.user.username, password=oldPassword)
        if user:
            # user = MyUser.objects.get(username=request.user)
            user.set_password(newPassword)
            user.save()
            return JsonResponse({"status": "成功"})
        else:
            return JsonResponse({"status": "密码错误"})


class RequestLog(View):
    def get(self, request):
        # 查询这个学生参与的所有会议
        student_obj = Student.objects.filter(sno=request.user.username)
        meeting_list = []
        if student_obj:
            meeting_list = student_obj[0].meeting_student.all()

        context = {
            "meeting_list": meeting_list
        }
        print(meeting_list)

        return render(request, template_name="dataManagement/requestLog.html", context=context)

    def post(self, request):
        pass


class RequestLogShow(View):
    def get(self, request):
        meeting_id = request.GET.get("meeting_id")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        # 获取学生对象
        student_obj = get_object_or_404(Student, sno=request.user.username)
        application_forms_student = meeting_obj.meeting_for_applicationform.filter(sno=request.user.username)
        application_form_student = []
        student_academicActivityImages = ""
        student_publicationsImages = ""
        student_participateItemsImages = ""
        if application_forms_student:
            application_form_student = application_forms_student[0]
            # 学术活动
            student_academicActivityImages = application_form_student.student_academicActivityImage.all()
            # 发表论文
            student_publicationsImages = application_form_student.student_publicationsImage.all()
            # 参与项目
            student_participateItemsImages = application_form_student.student_participateItemsImage.all()
            # 科研活动
            student_researchProjectsImages = application_form_student.student_researchProjectsImage.all()
            # 研究生创新项目
            student_innovationProjectsImages = application_form_student.student_innovationProjectsImage.all()
            # 社会服务
            student_socialWorkImages = application_form_student.student_socialWorkImage.all()
        # 学术活动

        context = {
            "application_form_student": application_form_student,
            "student_obj": student_obj,
            "student_academicActivityImages": student_academicActivityImages,
            "student_publicationsImages": student_publicationsImages,
            "student_participateItemsImages": student_participateItemsImages,
            "student_researchProjectsImages": student_researchProjectsImages,
            "student_innovationProjectsImages": student_innovationProjectsImages,
            "student_socialWorkImages": student_socialWorkImages,

        }
        return render(request, template_name="dataManagement/applicationFormShow.html", context=context)

    # 用来提交
    def post(self, request):
        print(request.POST)
        return JsonResponse({'status': "成功"})


class ApplicationFormUpload(View):
    def post(self, request):
        meeting_id = request.POST.get("meeting_id")
        application_form_id = request.POST.get("application_form_id")
        file = request.FILES.get("file_data")
        file_about = request.POST.get("file_about")
        # # 获取会议
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        # # 获取申请表
        application_obj_list = ApplicationForm.objects.filter(pk=application_form_id)
        if not application_obj_list:
            # 获取学生
            student_obj = get_object_or_404(Student, sno=request.user.username)
            # 创建赋分表
            application_obj = ApplicationForm.objects.create(student=student_obj, sno=student_obj.sno,meeting=meeting_obj, sname=student_obj.sname)
        else:
            application_obj = get_object_or_404(ApplicationForm, pk=application_form_id)
        if file_about == "学术活动":
            AcademicActivity.objects.create(applicationForm=application_obj, academicActivityImage=file)
        elif file_about == "发表论文":
            Publications.objects.create(applicationForm=application_obj, academicActivityImage=file)
        elif file_about == "参与项目":
            ParticipateItems.objects.create(applicationForm=application_obj, academicActivityImage=file)
        elif file_about == "科研项目":
            ResearchProjects.objects.create(applicationForm=application_obj, academicActivityImage=file)
        elif file_about == "研究生创新项目":
            InnovationProjects.objects.create(applicationForm=application_obj, academicActivityImage=file)
        elif file_about == "社会服务":
            SocialWork.objects.create(applicationForm=application_obj, academicActivityImage=file)

        return JsonResponse({'status': "成功"})


#  删除单个文件
class DeleteOne(View):
    def post(self, request):
        image_id = request.POST.get('key')
        file_about = request.POST.get('file_about')
        if file_about == "学术活动":
            academicActivityImage = AcademicActivity.objects.filter(pk=image_id)
            if academicActivityImage:
                academicActivityImage[0].delete()
            else:
                return JsonResponse({"status": "该文件不存在"})
        elif file_about == "发表论文":
            publications = ParticipateItems.objects.filter(pk=image_id)
            if publications:
                publications[0].delete()
            else:
                return JsonResponse({"status": "该文件不存在"})
        elif file_about == "参与项目":
            participateItems = ParticipateItems.objects.filter(pk=image_id)
            if participateItems:
                participateItems[0].delete()
            else:
                return JsonResponse({"status": "该文件不存在"})
        elif file_about == "科研项目":
            researchProjects = ResearchProjects.objects.filter(pk=image_id)
            if researchProjects:
                researchProjects[0].delete()
            else:
                return JsonResponse({"status": "该文件不存在"})
        elif file_about == "研究生创新项目":
            innovationProjects = InnovationProjects.objects.filter(pk=image_id)
            if innovationProjects:
                innovationProjects[0].delete()
            else:
                return JsonResponse({"status": "该文件不存在"})
        elif file_about == "社会服务":
            socialWorks = SocialWork.objects.filter(pk=image_id)
            if socialWorks:
                socialWorks[0].delete()
            else:
                return JsonResponse({"status": "该文件不存在"})

        return JsonResponse({"status": "成功"})


class DeleteAll(View):
    def post(self, request):
        pass