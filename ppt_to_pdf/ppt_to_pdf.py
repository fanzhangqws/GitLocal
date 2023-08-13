import comtypes.client
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics,ttfonts
import numpy as np
import pandas as pd
import smtplib
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from email.mime.application import MIMEApplication
from smtplib import SMTP_SSL

def init_powerpoint():
   powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
   powerpoint.Visible = 1
   return powerpoint

def ppt_to_pdf(powerpoint, inputFileName, outputFileName, formatType = 32):
   if outputFileName[-3:] != 'pdf':
       outputFileName = outputFileName + ".pdf"
   deck = powerpoint.Presentations.Open(inputFileName)
   deck.SaveAs(outputFileName, formatType) # formatType = 32 for ppt to pdf
   deck.Close()

def convert_files_in_folder(powerpoint, folder):
   files = os.listdir(folder)
   pptfiles = [f for f in files if f.endswith((".ppt", ".pptx"))]
   for pptfile in pptfiles:
       fullpath = os.path.join(cwd, pptfile)
       fullpath_out = os.path.join(cwd, 'pdf_version.pdf')
       ppt_to_pdf(powerpoint, fullpath, fullpath_out)

def create_watermark(content, file_name):
    """水印信息"""
    # 默认大小为21cm*29.7cm
    # file_name = "mark.pdf"
    c = canvas.Canvas(file_name, pagesize=(100*cm, 100*cm))
    # 移动坐标原点(坐标系左下为(0,0))
    c.translate(1*cm, 1*cm)
    # 注册字体
    pdfmetrics.registerFont (ttfonts.TTFont ('song', 'STXINWEI.ttf')) 
    # 设置字体
    c.setFont ('song', 20) # 设置字体及大小
    # 指定描边的颜色
    c.setStrokeColorRGB(0, 1, 0)
    # 指定填充颜色
    c.setFillColorRGB(0, 1, 0)
    # 旋转45度,坐标系被旋转
    c.rotate(30)
    # 指定填充颜色
    c.setFillColorRGB(0, 0, 0, 0.1)
    # 画几个文本,注意坐标系旋转的影响
    for i in np.arange(1,30,10):
        for j in np.arange(-50,80,1):
            c.drawString(i*cm, j*cm, content)

    c.setFillAlpha(0.6)
    # 关闭并保存pdf文件
    c.save()
    return file_name

def add_watermark(pdf_file_in, pdf_file_mark, pdf_file_out):
    """把水印添加到pdf中"""
    pdf_output = PdfFileWriter()
    input_stream = open(pdf_file_in, 'rb')
    pdf_input = PdfFileReader(input_stream, strict=False)

    # 获取PDF文件的页数
    pageNum = pdf_input.getNumPages()

    # 读入水印pdf文件
    pdf_watermark = PdfFileReader(open(pdf_file_mark, 'rb'), strict=False)
    # 给每一页打水印
    for i in range(pageNum):
        page = pdf_input.getPage(i)
        page.mergePage(pdf_watermark.getPage(0))
        page.compressContentStreams()  # 压缩内容
        pdf_output.addPage(page)
    pdf_output.write(open(pdf_file_out, 'wb'))

def sendmail(subject,msg,toaddrs,ccaddress,fromaddr,smtpaddr,password,pdfFile=None):
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
    if ccaddress[0]!='':
        mail_msg['Cc'] = ','.join(ccaddress)
    mail_msg.attach(MIMEText(msg, 'html', 'utf-8')) #发送html格式邮件

    part = MIMEApplication(open(pdfFile, 'rb').read()) 
    part.add_header('Content-Disposition', 'attachment', filename='水印文件.pdf') 
    mail_msg.attach(part)

    
    try:
        s = smtplib.SMTP()
        s.connect(smtpaddr,25) #连接smtp服务器
        s.login(fromaddr,password) #登录邮箱
        if ccaddress[0]!='':
            s.sendmail(fromaddr, [toaddrs,ccaddress], mail_msg.as_string())
        else:
            s.sendmail(fromaddr, toaddrs, mail_msg.as_string()) #发送邮件
        s.quit()
        print ("邮件发送成功！")
    except Exception as e:
        print("Error: unable to send email")
        print(e)

if __name__ == "__main__":
    powerpoint = init_powerpoint()
    cwd = os.getcwd()
    convert_files_in_folder(powerpoint, cwd)
    powerpoint.Quit()

    
    fromaddr = input('请输入发送人邮箱地址：')
    smtpaddr = "x.x.x.x"
    password = input('请输入发送人邮箱密码：')
    subject = input('请输入邮件标题：')
    msg = input('请输入邮件内容：')

    match_table = pd.read_excel('邮件地址表.xlsx')
    match_table.fillna('',inplace=True)
    if os.path.exists('水印结果'):
        pass
    else:
        os.mkdir('水印结果')
    if os.path.exists('pdf结果'):
        pass
    else:
        os.mkdir('pdf结果')

    mask_data_folder = os.path.join(os.getcwd(), '水印结果') #文件路径
    pdf_data_folder_out = os.path.join(os.getcwd(), 'pdf结果') #文件路径
    pdf_file_in = os.path.realpath('pdf_version.pdf')
    for i in range(len(match_table)):
        content = match_table.loc[i,'水印内容']
        email_address = [match_table.loc[i,'对应邮箱']]
        cc_address = [match_table.loc[i,'抄送邮箱']]
        water_mask_file_name = os.path.join(mask_data_folder, content+'.pdf')
        pdf_file_out = os.path.join(pdf_data_folder_out, content+'.pdf')
        if os.path.exists(water_mask_file_name):
            print('水印： '+content+' 已存在，不再重复生成。')
            pdf_file_mark = water_mask_file_name
        else:
            print('正在生成水印： '+content)
            pdf_file_mark = create_watermark(content, water_mask_file_name)

        print('正在给文件打水印： '+content)
        add_watermark(pdf_file_in, pdf_file_mark, pdf_file_out)
        print('正在发送邮件给 '+ email_address[0])
        sendmail(subject,msg,email_address,cc_address,fromaddr,smtpaddr,password,pdf_file_out)