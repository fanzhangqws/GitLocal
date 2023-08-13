# -*- coding: utf-8 -*-
from servicerequest import ServiceRequest
from base import Session, engine, Base
from sqlalchemy import *
import time
import requests
import logging
import ftplib
import socket
from datetime import datetime
import os 
from logging.handlers import RotatingFileHandler
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'




log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = 'process_log/process4.log'
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=100, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)
app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

app_log.addHandler(my_handler)


while True:

    # generate database schema
    Base.metadata.create_all(engine)
    session = Session()

    try:

        server = ftplib.FTP()
        server.connect('133.68.255.73', 21)
        server.login('ctccxa','P@ssw0rd')
        server.encoding='gbk'
        file_list = server.nlst()

        for file in file_list:
            if file.startswith('CQ_ fault'):
                # print(file)
                gFile = open('ftp_data/%s'%(file), "wb")
                server.retrbinary('RETR %s'%(file), gFile.write)
                gFile.close()
                
                gFile = open('ftp_data/%s'%(file), "r")
                buff = gFile.read()
                for line in buff.split('\n'):
                    if len(line)>0:
                        raw_data = line.split(',')
                        if session.query(ServiceRequest).filter(ServiceRequest.serialuserid==raw_data[0],
                            ServiceRequest.finish_status==None).one_or_none() is not None:
                            session.query(ServiceRequest).filter(
                                ServiceRequest.serialuserid==raw_data[0],ServiceRequest.finish_status==None
                                ).update({ServiceRequest.finish_status: raw_data[1], 
                                ServiceRequest.last_modify_time: datetime.now(),
                                ServiceRequest.return_date: datetime.now()})
                            session.commit()
                            app_log.info('set finish_status as %s to all order with serialuserid: %s'
                                %(raw_data[1], raw_data[0]))

                gFile.close()     

        server.quit()
        session.close()
        # wait for 5 mins
        t_duration = 300
        time.sleep(t_duration)
    except Exception as e:
        import traceback
        traceback.print_stack()
        errcode = -1
        errmsg = repr(e)
        # auto-debug based on errmsg
        app_log.error(errmsg)
        session.close()
        pass
