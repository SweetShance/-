from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.views import View
from django.db.models import Q
import datetime, random
from MyUser.models import MyUser
from dataManagement.models import Student, Teacher, Meeting, ApplicationForm, AcademicActivity, Publications,\
    ParticipateItems, ResearchProjects, InnovationProjects, SocialWork, delete_academicActivityImage, delete_innovationProjects,delete_participateItems,\
    delete_publicationsImage, delete_researchProjects, delete_socialWork, Qualification, OtherStudentGrade


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
        student_objs = Student.objects.filter(sno=request.user.username)
        if student_objs:
            student_obj = student_objs[0]
        # 首先判断当前学生在该会议中是否有资格
        print(meeting_obj)
        qualifications = meeting_obj.meeting_for_student.filter(sno=request.user.username)
        if qualifications or not student_objs:
            # 原因
            context = {
                "meeting_obj": meeting_obj,
                "status": "没有资格",
                "qualification": qualifications[0].text
            }
        else:
            application_forms_student = meeting_obj.meeting_for_applicationform.filter(sno=request.user.username)
            if not application_forms_student:
                application_form_student= ApplicationForm.objects.create(student=student_obj, sno=student_obj.sno,
                                                                 meeting=meeting_obj, sname=student_obj.sname)
            else:
                application_form_student = application_forms_student[0]
            student_academicActivityImages = ""
            student_publicationsImages = ""
            student_participateItemsImages = ""
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
            # endTime =  meeting_obj.endTime
            # 时间判断
            context = {
                "meeting_obj": meeting_obj,
                "application_form_student": application_form_student,
                "student_obj": student_obj,
                "student_academicActivityImages": student_academicActivityImages,
                "student_publicationsImages": student_publicationsImages,
                "student_participateItemsImages": student_participateItemsImages,
                "student_researchProjectsImages": student_researchProjectsImages,
                "student_innovationProjectsImages": student_innovationProjectsImages,
                "student_socialWorkImages": student_socialWorkImages,
            }
            if datetime.datetime.now() > meeting_obj.endTime:
                context["timeStatus"] = "已结束"
        return render(request, template_name="dataManagement/applicationFormShow.html", context=context)

    # 用来提交
    def post(self, request):
        # 会议id
        meeting_id = request.POST.get("meeting_id")
        # 申请表
        application_form_id = request.POST.get("application_form_id")
        # 学生id
        student_id = request.POST.get("student_id")
        # 个人简介
        presentation = request.POST.get("presentation")
        # 四六级
        optionRadios = request.POST.get("optionsRadios")
        # 图片
        CETImage = request.FILES.get("CETimage")
        # 学术活动
        academicActivityText = request.POST.get('academicActivityText')
        # 发表论文
        publicationsText = request.POST.get("publicationsText")
        # 参与项目
        participateItemsText = request.POST.get("participateItemsText")
        # 科研项目
        researchProjectsText = request.POST.get("researchProjectsText")
        # 研究生创新项目
        innovationProjectsText = request.POST.get("innovationProjectsText")
        # 社会服务
        socialWorkText = request.POST.get("socialWorkText")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        # 获取学生对象
        student_obj = get_object_or_404(Student, pk=student_id)
        # 首先判断该学生有没有资格
        qualifications = meeting_obj.meeting_for_student.filter(sno=request.user.username)
        if datetime.datetime.now() > meeting_obj.endTime:
            context = {
                "status": "会议已结束"
            }
            return render(request, template_name="dataManagement/transfer.html", context=context)
        if qualifications:
            context = {
                "status": "不符合申请资格"
            }
            return render(request, template_name="dataManagement/transfer.html", context=context)
        else:
            applicationForms = ApplicationForm.objects.filter(pk=application_form_id)
            if applicationForms:
                applicationForm = applicationForms[0]
                applicationForm.presentation = presentation
                if CETImage:
                    applicationForm.cetImage = CETImage
                # 修改四六级 已经选过了
                if applicationForm.cetstatus:
                    if optionRadios != applicationForm.englishChoice:
                        # 新选的
                        if optionRadios == "四级":
                            student_obj.CET4Count += 1
                            student_obj.CET6Count -= 1
                            student_obj.save()
                        else:
                            student_obj.CET4Count -= 1
                            student_obj.CET6Count += 1
                            student_obj.save()
                else:
                    if optionRadios == "四级":
                        student_obj.CET4Count += 1
                        applicationForm.cetstatus = True
                        student_obj.save()
                    else:
                        student_obj.CET6Count += 1
                        applicationForm.cetstatus = True
                        student_obj.save()
                applicationForm.englishChoice = optionRadios
                applicationForm.academicActivityText = academicActivityText
                applicationForm.publicationsText = publicationsText
                applicationForm.participateItemsText = participateItemsText
                applicationForm.researchProjectsText = researchProjectsText
                applicationForm.innovationProjectsText = innovationProjectsText
                applicationForm.socialWorkText = socialWorkText
                applicationForm.save()
                context = {
                    "status": "提交成功",
                    "meeting_id": meeting_id
                }
                return render(request, template_name="dataManagement/transfer.html", context=context)


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
        data = {}
        if not application_obj_list:
            # 获取学生
            student_obj = get_object_or_404(Student, sno=request.user.username)
            # 创建赋分表
            application_obj = ApplicationForm.objects.create(student=student_obj, sno=student_obj.sno,meeting=meeting_obj, sname=student_obj.sname)
        else:
            application_obj = get_object_or_404(ApplicationForm, pk=application_form_id)
        if file_about == "学术活动":
            academicActivity_obj = AcademicActivity.objects.create(applicationForm=application_obj, name=file.name, academicActivityImage=file)
            data['image_id'] = academicActivity_obj.id
            data['file_about'] = "学术活动"
            data['status'] = "成功"
        elif file_about == "发表论文":
            publications_obj = Publications.objects.create(applicationForm=application_obj, name=file.name, publicationsImage=file)
            data['image_id'] = publications_obj.id
            data['file_about'] = "发表论文"
            data['status'] = "成功"
        elif file_about == "参与项目":
            participateItems_obj = ParticipateItems.objects.create(applicationForm=application_obj, name=file.name, participateItemsImage=file)
            data['image_id'] = participateItems_obj.id
            data['file_about'] = "参与项目"
            data['status'] = "成功"
        elif file_about == "科研项目":
            researchProjects_obj = ResearchProjects.objects.create(applicationForm=application_obj, name=file.name, researchProjectsImage=file)
            data['image_id'] = researchProjects_obj.id
            data['file_about'] = "科研项目"
            data['status'] = "成功"
        elif file_about == "研究生创新项目":
            innovationProjects_obj = InnovationProjects.objects.create(applicationForm=application_obj, name=file.name, innovationProjectsImage=file)
            data['image_id'] = innovationProjects_obj.id
            data['file_about'] = "研究生创新项目"
            data['status'] = "成功"
        elif file_about == "社会服务":
            socialWork_obj = SocialWork.objects.create(applicationForm=application_obj, name=file.name, socialWorkImage=file)
            data['image_id'] =socialWork_obj.id
            data['file_about'] = "社会服务"
            data['status'] = "成功"
        return JsonResponse(data)


#  删除单个文件
class DeleteOne(View):
    def post(self, request):
        image_id = request.POST.get('key')
        file_about = request.POST.get('file_about')
        if file_about == "学术活动":
            academicActivityImage = AcademicActivity.objects.filter(pk=image_id)
            if academicActivityImage:
                delete_academicActivityImage(academicActivityImage[0])
                academicActivityImage[0].delete()
            else:
                return JsonResponse({"status": "该文件不存在"})
        elif file_about == "发表论文":
            publications =  Publications.objects.filter(pk=image_id)
            if publications:
                delete_publicationsImage(publications[0])
                publications[0].delete()
            else:
                return JsonResponse({"status": "该文件不存在"})
        elif file_about == "参与项目":
            participateItems = ParticipateItems.objects.filter(pk=image_id)
            if participateItems:
                delete_participateItems(participateItems[0])
                participateItems[0].delete()
            else:
                return JsonResponse({"status": "该文件不存在"})
        elif file_about == "科研项目":
            researchProjects = ResearchProjects.objects.filter(pk=image_id)
            if researchProjects:
                delete_researchProjects(researchProjects[0])
                researchProjects[0].delete()
            else:
                return JsonResponse({"status": "该文件不存在"})
        elif file_about == "研究生创新项目":
            innovationProjects = InnovationProjects.objects.filter(pk=image_id)
            if innovationProjects:
                delete_innovationProjects(innovationProjects[0])
                innovationProjects[0].delete()
            else:
                return JsonResponse({"status": "该文件不存在"})
        elif file_about == "社会服务":
            socialWorks = SocialWork.objects.filter(pk=image_id)
            if socialWorks:
                delete_socialWork(socialWorks[0])
                socialWorks[0].delete()
            else:
                return JsonResponse({"status": "该文件不存在"})
        return JsonResponse({"status": "成功"})


# 学生互评
class PeerAssessment(View):
    def get(self, request):
        meeting_id = request.GET.get("meeting_id")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        # 看是否有资格
        qualifications = meeting_obj.meeting_for_student.filter(sno=request.user.username)
        if qualifications:
            context = {
                "this_status": qualifications[0].text,
                "meeting_obj": meeting_obj
            }
        else:
            # 判断是否有选择的人
            student_obj = Student.objects.get(sno=request.user.username)
            otherStudentGrade = OtherStudentGrade.objects.filter(student=student_obj, meeting=meeting_obj)
            if otherStudentGrade:
                application_form_student = otherStudentGrade[0].applicationForm
                student_academicActivityImages = ""
                student_publicationsImages = ""
                student_participateItemsImages = ""
                # 获取该学生赋分表的学生互评项目
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
                context = {
                    "meeting_obj": meeting_obj,
                    "application_form_student": application_form_student,
                    "student_obj": student_obj,
                    "student_academicActivityImages": student_academicActivityImages,
                    "student_publicationsImages": student_publicationsImages,
                    "student_participateItemsImages": student_participateItemsImages,
                    "student_researchProjectsImages": student_researchProjectsImages,
                    "student_innovationProjectsImages": student_innovationProjectsImages,
                    "student_socialWorkImages": student_socialWorkImages,
                    "student_otherGrade": otherStudentGrade[0].otherGrade
                }
                if otherStudentGrade[0].otherGrade:
                    context["status"] = "已完成"
            else:
                meeting_for_applicationforms = meeting_obj.meeting_for_applicationform.filter(~Q(sno=request.user.username),   otherstatus=False)
                if meeting_for_applicationforms:
                    application_form_student = meeting_for_applicationforms[random.randint(0, len(meeting_for_applicationforms)-1)]
                    OtherStudentGrade.objects.create(applicationForm=application_form_student, student=student_obj, meeting=meeting_obj)
                    # 加入到表中
                    student_academicActivityImages = ""
                    student_publicationsImages = ""
                    student_participateItemsImages = ""
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
                    context = {
                        "meeting_obj": meeting_obj,
                        "application_form_student": application_form_student,
                        "student_obj": student_obj,
                        "student_academicActivityImages": student_academicActivityImages,
                        "student_publicationsImages": student_publicationsImages,
                        "student_participateItemsImages": student_participateItemsImages,
                        "student_researchProjectsImages": student_researchProjectsImages,
                        "student_innovationProjectsImages": student_innovationProjectsImages,
                        "student_socialWorkImages": student_socialWorkImages,
                    }
                else:
                    context = {
                        "this_status": "暂无可评学生请稍后评分!",
                        "meeting_obj": meeting_obj
                    }

        return render(request, template_name="dataManagement/peerAssessment.html", context=context)

    def post(self, request):
        meeting_id = request.POST.get("meeting_id")
        applicationFormId = request.POST.get("applicationFormId")
        number = request.POST.get("number")
        student_obj = get_object_or_404(Student, sno=request.user.username)
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        applicationForm_obj = get_object_or_404(ApplicationForm, pk=applicationFormId)
        # 查找是否被评分
        otherGrade_obj = OtherStudentGrade.objects.filter(applicationForm=applicationForm_obj, student=student_obj, meeting=meeting_obj)
        if otherGrade_obj:
            if otherGrade_obj[0].otherGrade:
                return JsonResponse({"status": "该学生已被评分"})
            else:
                otherGrade_obj[0].otherGrade = number
                otherGrade_obj[0].save()
                return JsonResponse({"status": "成功"})
        # else:
        #     OtherStudentGrade.objects.create(applicationForm=applicationForm_obj, student=student_obj, otherGrade=number, meeting=meeting_obj)
            return JsonResponse({"status": "成功"})