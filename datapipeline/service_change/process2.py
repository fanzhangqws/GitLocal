# -*- coding: utf-8 -*-
from servicechange import ServiceChange, OrderStatusTable
from base import Session, engine, Base
from sqlalchemy import *
import time
import zeep
import requests
from zeep.transports import Transport
from requests.exceptions import RequestException
from datetime import datetime
import os 
import logging
from logging.handlers import RotatingFileHandler
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'




log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = 'process_log/process2.log'
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=100, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)

# logging.addHandler(my_handler)


app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

app_log.addHandler(my_handler)


while True:
    # internet webservice connection
    session_web = requests.Session()
    session_web.verify = False
    transport = Transport(session=session_web)
    wsdl = 'http://x.x.x.x:x/serviceList.asmx?WSDL'
    client = zeep.Client(wsdl=wsdl, transport=transport)

    # generate database schema
    Base.metadata.create_all(engine)
    session = Session()

    try:
        # get CO list
        co_list = []
        for query in session.query(ServiceChange):
            if query.CO not in co_list:
                co_list.append(query.CO)

        for co_item in co_list:
            # all order
            ServiceChange_querys_part2 = session.query(ServiceChange).filter(ServiceChange.CO==co_item, 
                ServiceChange.send_status=='0')
            cout_num=0
            for query_item in ServiceChange_querys_part2:
                try:
                    # send data to Changqing
                    result = None
                    if query_item.servicecode=='IPTV-Bridg':
                        cout_num+=1
                    if cout_num==2 and query_item.servicecode=='IPTV-Bridg':
                        servicecode='IPTV-Bridg2'
                    else:
                        servicecode=query_item.servicecode
                    result = client.service.ServiceChange(op=query_item.op, 
                        serialuserid=query_item.serialuserid, customerid=query_item.customerid,
                        name=query_item.name, cardtype=query_item.cardtype, 
                        idcardnum=query_item.idcardnum, servicecode=servicecode,
                        location=query_item.location, ordertype=query_item.ordertype, 
                        parameters=query_item.parameters)
                
                    # if result == '3501005':
                    session.query(ServiceChange).filter(ServiceChange.id == query_item.id).update(
                        {ServiceChange.send_status: '1', ServiceChange.succeed_status: '1',
                        ServiceChange.last_modify_time: datetime.now(), 
                        ServiceChange.errormsg:result})

                    session.query(OrderStatusTable).filter(OrderStatusTable.serialuserid==query_item.serialuserid
                        ).update({OrderStatusTable.send_date: datetime.now()})

                    session.commit()
                    app_log.info('%s succeed! serialuserid: %s'%(query_item.servicecode, 
                        query_item.serialuserid))
                    app_log.info('set send_date to %s, serialuserid: %s'%(query_item.servicecode, 
                        query_item.serialuserid))
                except Exception as e:
                    # fail status
                    result= result or '无返回结果'
                    session.query(ServiceChange).filter(ServiceChange.id==query_item.id).update(
                        {ServiceChange.send_status: '1', ServiceChange.succeed_status: '0',
                        ServiceChange.last_modify_time: datetime.now(), 
                        ServiceChange.errormsg:result})
                    session.commit()
                    app_log.error('%s fail! serialuserid: %s, error message: %s'%(
                        query_item.servicecode, query_item.serialuserid, result))
                    raise
        session.close()
        # wait for 5 mins
        time.sleep(300)

    except RequestException as e:
        import traceback
        traceback.print_stack()
        errcode = -1
        errmsg = repr(e)

        # auto-debug based on errmsg
        app_log.error(errmsg)
        # wait for 1s
        time.sleep(1)
        session.close()

    except Exception as e:
        import traceback
        traceback.print_stack()
        errcode = -1
        errmsg = repr(e)

        # auto-debug based on errmsg
        app_log.error(errmsg)
        # wait for 5 mins
        time.sleep(300)
        session.close()
        pass