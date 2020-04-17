#使用celery
from celery import Celery
from django.core.mail import send_mail  #django自带发送邮件功能
from django.conf import settings    #使用settings.py里面的参数
from email.mime.text import MIMEText
import smtplib, random
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr

#创建一个Celery类的实例对象
app = Celery("celsey_tasks.tasks", broker='redis://127.0.0.1:6379/8', backend='redis://127.0.0.1:6379/9')

#定义任务函数
@app.task
def send_register_active_email(to_email_addr, token):
    # 发邮件
    msg = MIMEText('%s, 你好!你的验证码为:<span style="color:#87CEFA">%s</span>'%(to_email_addr, token), 'html', 'utf-8')
    from_addr = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD  # 验证码

    to_addr = to_email_addr
    smtp_server = "smtp.163.com"
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = "新疆农业大学奖助学金评定系统"
    server = smtplib.SMTP(smtp_server, 25)
    # server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
