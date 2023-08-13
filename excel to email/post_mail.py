import os
import smtplib
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from email.mime.application import MIMEApplication
from smtplib import SMTP_SSL


def sendmail(subject,msg,toaddrs,fromaddr,smtpaddr,password):
    '''
    @subject:邮件主题
    @msg:邮件内容
    @toaddrs:收信人的邮箱地址
    @fromaddr:发信人的邮箱地址
    @smtpaddr:smtp服务地址，可以在邮箱看，比如163邮箱为smtp.163.com
    @password:发信人的邮箱密码
    '''
    mail_msg = MIMEMultipart()
    mail_msg['Subject'] = subject
    mail_msg['From'] =fromaddr
    mail_msg['To'] = ','.join(toaddrs)
    mail_msg.attach(MIMEText(msg, 'html', 'utf-8')) #发送html格式邮件
    
    try:
        s = smtplib.SMTP()
        s.connect(smtpaddr,25) #连接smtp服务器
        s.login(fromaddr,password) #登录邮箱
        s.sendmail(fromaddr, toaddrs, mail_msg.as_string()) #发送邮件
        s.quit()
        print ("邮件发送成功！")
    except Exception as e:
        print("Error: unable to send email")
        print(e)

if __name__ == '__main__':
    df = pd.read_excel('xxxxx.xlsx')

    fromaddr = input('请输入发送人邮箱地址：')
    smtpaddr = "x.x.x.x"
    subject = "xxx"
    password = input('请输入发送人邮箱密码：')
    for i in range(len(df)):
        email_address = df.iloc[i]['邮箱地址']
        print(df.iloc[i]['邮箱地址'])
        toaddrs = [df.iloc[i]['邮箱地址']]
        msg="""
        <!DOCTYPE html>
        <html>
        <meta charset="utf-8">
        <head>
        <style>
        body { line-height: 1.5; }
        body { font-size: 10.5pt; color: rgb(0, 0, 0); line-height: 1.5;}
        table
          {
          border-collapse:collapse;
          }
        </style>
        </head>
        <body>
        <div id="container">
            <div id="content">
                <p>
                    <table id="tbl1" border="1">
                        <tr>
                            <td><strong>xx1</strong></td>
                            <td><strong>xx2</strong></td>
                        </tr>
                        <tr>                       
                            <td>""" + str(df.iloc[i]["所在部室 "]) + """</td>
                            <td>""" + str(df.iloc[i]["所在班组 "]) + """</td>
                        </tr>
                    </table>
                </p>
            </div>
        </div>
        </body>
        </html>
        """
        sendmail(subject,msg,toaddrs,fromaddr,smtpaddr,password)