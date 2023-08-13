# -*- coding: utf-8 -*-
from servicechange import ServiceChange, OrderStatusTable
from base import Session, engine, Base
from sqlalchemy import *
import time
from datetime import datetime
import logging
import os 
from logging.handlers import RotatingFileHandler
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'




log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = 'process_log/process1_1.log'
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

    CDCOSS = Table('v_changqing2', Base.metadata, autoload=True, autoload_with=engine)
    try:
        # get CO list
        co_list = []
        for query in session.query(CDCOSS):
            if query.co not in co_list:
                co_list.append(query.co)

        for co_item in co_list:       
            # other order type
            other_order = session.query(CDCOSS).filter(CDCOSS.columns.co==co_item)
            for query in other_order:
                app_log.info('get %s data from CDCOSS, serialuserid: %s, co: %s'%(query.servicecode, query.so, query.co))
                op='CT-COM-XA'
                serialuserid=query.so
                customerid=query.customerid
                name=query.name
                appl_date = query.appl_date
                co = query.co
                send_status='0'
                succeed_status='0'
                last_modify_time = datetime.now()
                errormsg=''
                parameters = ''
                if query.cardtype in ['身份证','其他']:
                    cardtype=query.cardtype
                    idcardnum=query.idcardnum
                else:
                    raise ValueError("Invalid cardtype!")

                location=query.location
                if query.servicecode=='宽带':
                    servicecode='Internet-Bridge'
                elif query.servicecode=='网络电视(IPTV)':
                    servicecode='IPTV-Bridg'
                elif query.servicecode=='普通电话接入':
                    servicecode='VOIP-Route-PPP'
                else:
                    raise ValueError("Invalid servicecode!")


                if query.ordertype=='停机':
                    ordertype='6'
                elif query.ordertype=='复机':
                    ordertype='7'
                else:
                    raise ValueError("Invalid ordertype!")

                query_element = session.query(ServiceChange).filter(ServiceChange.serialuserid==query.so
                    ).one_or_none()
                if query_element is None:
                    # query_element = ServiceChange()
                    # merge data to ServiceChange, if data exist, then update, else insert data
                    session.add(ServiceChange(op=op, serialuserid=serialuserid, 
                        customerid=customerid, name=name, cardtype=cardtype, idcardnum=idcardnum, 
                        servicecode=servicecode, location=location, ordertype=ordertype, CO=co, 
                        parameters=parameters, succeed_status=succeed_status,
                        send_status=send_status, last_modify_time=last_modify_time, errormsg=errormsg,
                        acc_nbr=query.acc_nbr))


                query_element2 = session.query(OrderStatusTable).filter(OrderStatusTable.serialuserid==query.so
                    ).one_or_none()
                if query_element2 is None:
                    # query_element2 = OrderStatusTable()
                    session.add(OrderStatusTable(serialuserid=serialuserid, CO=co, location=location, 
                        appl_date=appl_date, ordertype=ordertype))
                session.commit()
                app_log.info('write data to ServiceChange, serialuserid: %s, co: %s'%(serialuserid, co))
                app_log.info('write data to OrderStatusTable, serialuserid: %s, co: %s'%(serialuserid, co))

        session.close()
        # wait for 6 hours
        t_duration = 3600*6
        time.sleep(t_duration)

    except Exception as e:
        import traceback
        traceback.print_stack()
        errcode = -1
        errmsg = repr(e)

        # auto-debug based on errmsg
        app_log.error(errmsg)
        session.rollback()
        # wait for 1s
        time.sleep(1)
        session.close()
        pass
