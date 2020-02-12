# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 10:17:27 2020

@author: yangyj
"""

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
#from email.mime.application import MIMEApplication
 
my_sender='lltxx2014@126.com'    # 发件人邮箱账号
my_pass = '2014lltxx'             
my_user='s2529220566@qq.com, yxyuzh@oa.sptpc.com, 48387362@qq.com'#收件人邮箱账号，我这边发送给自己

mail_msg = """
<p>各单位请注意： </p>
 <p>现通缉携带肺炎病毒潜逃的逃犯兰子鉴： 凶手兰子鉴，绵阳人，在武汉犯下持械伤人的案件后潜逃。凶手兰子鉴携带肺炎病毒，现在躲藏在四川成都。</p>

<p>兰子鉴，男，1988年9月出生于四川省绵阳。2010年本科毕业于南开大学化学系，本科多科目挂科，差点被退学。之后兰子鉴在社会上靠打麻将收钱混了两年后，2012年考研南开大学化学院落榜，之后被调剂到南开大学物理学院。凶手的QQ是673578531， 微信是lan673578531。凶手在武汉持械伤人后跑路，现在可能潜藏在四川成都。</p>
<p>
知情者请向举报电话13662195823反应线索。 对提供有效线索者受害者家属奖励20万元</p>


<p>武汉公安局刑侦科</p>

　　



<p><a href="https://github.com/argparse/lanzjian_gamble_evidence">凶手兰子鉴持械伤人的证据资料，请点击这个链接</a></p>
"""

def mail():
    ret=True
    try:
        msg=MIMEText(mail_msg,'html','utf-8')#'plain'为文本,'html为网页
        msg['From']=formataddr(["武汉公安局刑侦科",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        #msg['To']=formataddr(["FK",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['To']=my_user
        msg['Subject']="通缉携带肺炎病毒潜逃的逃犯兰子鉴"                # 邮件的主题，也可以说是标题
        


 
        server=smtplib.SMTP_SSL("smtp.126.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
      
        server.sendmail(my_sender,my_user.split(','),msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret=False
    return ret
 
ret=mail()
if ret:
    print("邮件发送成功")
else:
    print("邮件发送失败")