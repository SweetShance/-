from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.views import View
from django.db.models import Q, F, SmallIntegerField, Sum
import datetime, random, json
from MyUser.models import MyUser
from dataManagement.models import Student, Teacher, Meeting, ApplicationForm, AcademicActivity, Publications,\
    ParticipateItems, ResearchProjects, InnovationProjects, SocialWork, delete_academicActivityImage, delete_innovationProjects,delete_participateItems,\
    delete_publicationsImage, delete_researchProjects, delete_socialWork, Qualification, OtherStudentGrade, MentorGrade, Message, ApplicationGrade


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


# 老师
class MeetingList(View):
    def get(self, request):
        # 获取所有会议
        meeting_obj_all = Meeting.objects.all()
        context = {
            "meeting_obj_all": meeting_obj_all
        }
        return render(request, template_name="dataManagement/MeetingList.html", context=context)


# 老师 会学生列表
class MeetingForMyStudent(View):
    def get(self, request):
        #
        meeting_id = request.GET.get("meeting_id")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        if request.user.identity == "老师":
            # 获取老师
            teacher_obj = get_object_or_404(Teacher, tno=request.user.username)
            # 获取当前会议中老师的所有学生
            meeting_student_list_application_qualification = []
            meeting_student_list = meeting_obj.student.filter(tutor=teacher_obj)
            for meeting_student in meeting_student_list:
                student_application_for_meeting = meeting_obj.meeting_for_applicationform.filter(student=meeting_student)
                # 资格
                student_qualification_for_meeting = meeting_obj.meeting_for_student.filter(sno=meeting_student.sno)

                if student_application_for_meeting and not student_qualification_for_meeting:
                    # 是否评分
                    mentorGrade_application_for_meeting = MentorGrade.objects.filter(applicationForm=student_application_for_meeting[0])
                    if mentorGrade_application_for_meeting:
                        meeting_student_list_application_qualification.append([meeting_student, "已提交", "有资格", "已评分"])
                    else:
                        meeting_student_list_application_qualification.append([meeting_student, "已提交", "有资格", "未评分"])
                elif not student_application_for_meeting and not student_qualification_for_meeting:
                    meeting_student_list_application_qualification.append([meeting_student, "未提交", "有资格", "未评分"])
                elif not student_application_for_meeting and student_qualification_for_meeting:
                    meeting_student_list_application_qualification.append([meeting_student, "未提交", "无资格", "未评分"])
            context = {
                "meeting_obj": meeting_obj,
                "meeting_student_list_application_qualification": meeting_student_list_application_qualification
            }
        else:
            context = {
                "this_status": "你的身份不是老师"
            }

        return render(request, template_name="dataManagement/meetingForMyStudent.html", context=context)


# 老师对自己的学生审核评分
class MeetingForMyStudentCheck(View):
    def get(self, request):
        meeting_id = request.GET.get("meeting_id")
        student_id = request.GET.get("student_id")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        student_obj = get_object_or_404(Student, pk=student_id)
        student_qualification = meeting_obj.meeting_for_student.filter(sno=student_obj.sno)
        if student_qualification:
            context = {
                "this_status": "该学生本次会议没有申请资格",
                "text": student_qualification[0].text,
                "meeting_obj": meeting_obj,
                "student_obj": student_obj,
            }
        else:
            # 申请表
            application_form_student = meeting_obj.meeting_for_applicationform.filter(student=student_obj)
            if application_form_student:
                application_form_student = application_form_student[0]
                # 相关文件
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
                # 获取该会议该学生申请表
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
                # 看当前学生导师是否已评分
                mentorGrade_objs = MentorGrade.objects.filter(applicationForm = application_form_student)
                if mentorGrade_objs:
                    context["mentorGrade_obj"] = mentorGrade_objs[0]
            else:
                context = {
                    "meeting_obj": meeting_obj,
                    "student_obj": student_obj,
                    "this_status": "该学生暂未提交申请"
                }
        return render(request, template_name="dataManagement/MeetingForMyStudentCheck.html", context=context)

    def post(self, request):
        # 获取会议
        meeting_id = request.POST.get("meeting_id")
        # 获取申请表
        applicationFormId = request.POST.get("applicationFormId")
        # 获取number
        number = request.POST.get("number")
        # 获取原因
        text = request.POST.get("text")
        # 获取申请表
        applicationForm_obj = get_object_or_404(ApplicationForm, pk=applicationFormId)
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        if number:
            mentoyGrade_obj = MentorGrade.objects.create(applicationForm=applicationForm_obj, meeting=meeting_obj, mentorGrade=number)
            applicationForm_obj.activity = True
            applicationForm_obj.save()
            return JsonResponse({"status": "成功"})
        elif text:
            # 创建信息表
            to_user = get_object_or_404(MyUser, username=applicationForm_obj.sno)
            message = Message.objects.create(form_user=request.user, to_user=to_user, text=text)
            return JsonResponse({"status": "成功"})
        return JsonResponse({"status": "失败"})


# 评委赋分
class JuryGradeMeetingList(View):
    def get(self, request):
        # 获取但钱老师所在的会议
        teacher_obj = get_object_or_404(Teacher, tno=request.user.username)
        meeting_list_for_Jury = Meeting.objects.filter(jury=teacher_obj)
        context = {
            "meeting_list_for_Jury": meeting_list_for_Jury
        }
        return render(request, template_name="dataManagement/JuryGradeMeetingList.html", context=context)


# 评委学生
class JuryGradeMeetingStudentList(View):
    def get(self, request):
        meeting_id = request.GET.get("meeting_id")
        # 判断当前老师是否提交主审
        teacher = get_object_or_404(Teacher, tno=request.user.username)
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        # 获取主审学生赋分表
        jury_chief_umpire_students_form = meeting_obj.meeting_for_applicationform.filter(jury=teacher)
        # 获取主审学生的总分数 按赋分表分类
        sum_grade_list = ApplicationGrade.objects.values('applicationForm').annotate(num=Sum('grade')).filter(teacher=teacher, meeting=meeting_obj, chief_umpire=True).order_by("applicationForm_id")
        jury_chief_umpire_application_grade_list = []
        # 如果主审学生全部评分
        if jury_chief_umpire_students_form.count() == sum_grade_list.count():
            for jury_chief_umpire_student_form in jury_chief_umpire_students_form:
                # 获取主审分数
                sum_grade_chief_umpirestudent_applicationForm = ApplicationGrade.objects.annotate(num=Sum('grade')).filter(teacher=teacher, meeting_id=meeting_obj, chief_umpire=True, applicationForm=jury_chief_umpire_student_form)
                if sum_grade_chief_umpirestudent_applicationForm:
                    jury_chief_umpire_application_grade_list.append([jury_chief_umpire_student_form,
                                                                    sum_grade_chief_umpirestudent_applicationForm[0]])
            # 获取该会议所有学生
            students_application_for_meeting_list = meeting_obj.meeting_for_applicationform.all()
            # 获取该会议所有学生及主审成绩
            all_students_grade_for_meeting_list = []
            for student_application_for_meeting in students_application_for_meeting_list:
                # 如果这个老师全部提交了
                if teacher in meeting_obj.referTeacher.all():
                    # 我提交的成绩
                    sum_grade_chief_umpire_student_applicationForm = ApplicationGrade.objects.annotate(
                        num=Sum('grade')).filter(meeting_id=meeting_obj, teacher=teacher,
                                                 applicationForm=student_application_for_meeting)
                    all_students_grade_for_meeting_list.append([student_application_for_meeting, sum_grade_chief_umpire_student_applicationForm])
                # 没有全部提交
                else:
                    # 获取其主审成绩
                    sum_grade_chief_umpirestudent_applicationForm = ApplicationGrade.objects.annotate(num=Sum('grade')).filter(meeting_id=meeting_obj, chief_umpire=True, applicationForm=student_application_for_meeting)
                    if sum_grade_chief_umpirestudent_applicationForm:
                        # 添加到列表
                        all_students_grade_for_meeting_list.append([student_application_for_meeting, sum_grade_chief_umpirestudent_applicationForm])
                    else:
                        all_students_grade_for_meeting_list.append([student_application_for_meeting, '主审暂未提交'])
            context = {
                "jury_chief_umpire_application_grade_list": jury_chief_umpire_application_grade_list,
                "all_students_grade_for_meeting_list": all_students_grade_for_meeting_list,
                "status": "该主审已提交",
                "meeting_obj": meeting_obj
            }
        else:
            # 只获取我的主审学生成绩
            for jury_chief_umpire_student_form in jury_chief_umpire_students_form:
                # 获取主审分数
                sum_grade_chief_umpirestudent_applicationForm = ApplicationGrade.objects.annotate(num=Sum('grade')).filter(teacher=teacher, meeting_id=meeting_obj, chief_umpire=True, applicationForm=jury_chief_umpire_student_form)
                if sum_grade_chief_umpirestudent_applicationForm:
                    jury_chief_umpire_application_grade_list.append([jury_chief_umpire_student_form,
                                                                    sum_grade_chief_umpirestudent_applicationForm[0]])
                else:
                    jury_chief_umpire_application_grade_list.append([jury_chief_umpire_student_form,
                                                                    "暂未评分"])
            context = {
                "jury_chief_umpire_application_grade_list": jury_chief_umpire_application_grade_list,
                "status": "该主审未提交",
                "meeting_obj": meeting_obj
            }
            # 当前会议获取主审学生的赋分表
        # jury_chief_umpire_students_form = meeting_obj.meeting_for_applicationform.filter(jury=teacher)
        # # 获取申请表赋分里该老师的学生
        # #  判断主审是否提交
        # jury_chief_umpire_students_grade = []
        # tag = True
        # context = {}
        # for jury_chief_umpire_student_form in jury_chief_umpire_students_form:
        #     meeting_student_application_grade = Grade.objects.filter(applicationForm=jury_chief_umpire_student_form, teacher=teacher)
        #     if not meeting_student_application_grade: # 主审未提交(有一个主审学生成绩未查到)
        #         tag = False
        #     jury_chief_umpire_students_grade.append(Grade.objects.annotate(grade_all=F("englishGrade") + F("baseGrade") + F("academicActivityGrade") + F("publicationsGrade") + F("participateItemsGrade") + F("researchProjectsGrade") + F("innovationProjectsGrade") + F("socialWorkGrade")).filter(applicationForm=jury_chief_umpire_student_form))
        #
        # if not tag:
        #
        #     # 获取主审的学生
        #     context = {
        #         "this_status": "主审未提交",
        #         "jury_chief_umpire_students": jury_chief_umpire_students_grade,
        #     }
        #
        # if tag:
        #     # 主审已提交 获取所有学生和当前老师的主审学生及成绩
        #     meeting_student_application_list_grade = Grade.objects.annotate(grade_all=F("englishGrade") + F("baseGrade") + F("academicActivityGrade") + F("publicationsGrade") + F("participateItemsGrade") + F("researchProjectsGrade") + F("innovationProjectsGrade") + F("socialWorkGrade")).filter(meeting=meeting_obj)
        #     context = {
        #         "this_status": "主审已提交",
        #         "jury_chief_umpire_students": jury_chief_umpire_students_grade,
        #         "meeting_student_application_list": meeting_student_application_list_grade
        #     }
        return render(request, template_name="dataManagement/juryMeetingStudentList.html", context=context)


# 评委打分时学生信息展示
class JuryStudentApplicationFormShow(View):
    def get(self, request):
        meeting_id = request.GET.get("meeting_id")
        student_id = request.GET.get("student_id")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        student_obj = get_object_or_404(Student, pk=student_id)
        student_qualification = meeting_obj.meeting_for_student.filter(sno=student_obj.sno)
        if student_qualification:
            context = {
                "this_status": "该学生本次会议没有申请资格",
                "text": student_qualification[0].text,
                "meeting_obj": meeting_obj,
                "student_obj": student_obj,
            }
        else:
            # 申请表
            application_form_student = meeting_obj.meeting_for_applicationform.filter(student=student_obj)
            if application_form_student:
                application_form_student = application_form_student[0]
                # 相关文件
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
                # 获取赋分表
                fuItem_list = application_form_student.fuTable.fuItem.all()
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
                    "fuItem_list": fuItem_list
                }
            else:
                context = {
                    "meeting_obj": meeting_obj,
                    "student_obj": student_obj,
                    "this_status": "该学生暂未提交申请"
                }
        return render(request, template_name="dataManagement/juryMark.html", context=context)

    def post(self, request):
        meeting_id = request.POST.get("meeting_id")
        applicatinFormId = request.POST.get("applicatinFormId")
        data = request.POST.get("data") # 获取的是一json字符串 使用json.loads 来展开,
        print(meeting_id, applicatinFormId, data)
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        applicatinForm_obj = get_object_or_404(ApplicationForm, pk=applicatinFormId)
        # 获取主审的赋分表
        teacher = get_object_or_404(Teacher, username=request.user.username)
        jury_chief_umpire_students_form = meeting_obj.meeting_for_applicationform.filter(jury=teacher)

        # 遍历 data 并创建
        for number in json.loads(data):
            if applicatinForm_obj in jury_chief_umpire_students_form:
                ApplicationGrade.objects.create(teacher=teacher, applicationForm=applicatinForm_obj, meeting=meeting_obj, grade=number, chief_umpire=True)
            else:
                ApplicationGrade.objects.create(teacher=teacher, applicationForm=applicatinForm_obj, meeting=meeting_obj, grade=number, chief_umpire=False)

        return JsonResponse({"status": "成功"})









