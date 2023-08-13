from servicerequest import ServiceRequest
from base import Session, engine, Base
from sqlalchemy import *
import time
import zeep
import requests
from zeep.transports import Transport
from datetime import datetime
import logging
import os 
from logging.handlers import RotatingFileHandler
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'




log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = 'process_log/process2.log'
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=100, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)
app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

app_log.addHandler(my_handler)

# internet webservice connection
session_web = requests.Session()
session_web.verify = False
transport = Transport(session=session_web)
wsdl = 'http://xx.xx.xx.xx:xxxx/serviceList.asmx?WSDL'
client = zeep.Client(wsdl=wsdl, transport=transport)

# generate database schema
Base.metadata.create_all(engine)
session = Session()

result_status_map = {
    '3501005':'接口调用成功',
    '3501006':'接口调用异常',
    '3501051':'无效参数值',
    '3501052':'拒绝请求(未说明原因)',
    '3501053':'内部错误',
}

while True:
    try:
        # other order
        ServiceRequest_querys = session.query(ServiceRequest).filter(ServiceRequest.send_status=='0')
        for query_item in ServiceRequest_querys:
            # send data to Changqing
            result = client.service.ServiceRequest(op=query_item.op, serialuserid=query_item.serialuserid, 
            	customerid=query_item.customerid,name=query_item.name,
            	address=query_item.address, contact=query_item.contact, tel=query_item.tel,
            	location=query_item.location, mobile=query_item.mobile, faulttype=query_item.faulttype, 
            	faultdetail=query_item.faultdetail, other=query_item.other)
            result = result.split(':')[1]
            if result == '3501005':
                session.query(ServiceRequest).filter(ServiceRequest.id == query_item.id).update(
                    {ServiceRequest.send_status: '1', ServiceRequest.succeed_status: '1',
                    ServiceRequest.last_modify_time: datetime.now(),
                    ServiceRequest.send_date: datetime.now()})
                session.commit()
                app_log.info('ServiceRequest succeed! serialuserid: %s'%(query_item.serialuserid))
            else:
                # fail status
                session.query(ServiceRequest).filter(ServiceRequest.id==query_item.id).update(
                    {ServiceRequest.send_status: '1', ServiceRequest.succeed_status: '0',
                    ServiceRequest.last_modify_time: datetime.now(), 
                    ServiceRequest.errormsg:result_status_map[result]})
                session.commit()
                app_log.error('ServiceRequest fail! serialuserid: %s, error message: %s'%(
                	query_item.serialuserid, result_status_map[result]))
        
        session.close()
        # wait for 5 mins
        time.sleep(300)

    except Exception as e:
        import traceback
        traceback.print_stack()
        errcode = -1
        errmsg = repr(e)

        # auto-debug based on errmsg
        app_log.error(errmsg)
        session.close()
        # wait for 1s
        time.sleep(1)

        pass