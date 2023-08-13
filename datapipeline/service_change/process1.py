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
logFile = 'process_log/process1.log'
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

    CDCOSS = Table('v_changqing', Base.metadata, autoload=True, autoload_with=engine)

    try:
        # get CO list
        co_list = []
        for query in session.query(CDCOSS):
            if query.co not in co_list:
                co_list.append(query.co)

        for co_item in co_list:
            new_order = session.query(CDCOSS).filter(CDCOSS.columns.co==co_item, 
                CDCOSS.columns.ordertype=='新装')
            if new_order.count()>0:
                query=new_order[0]
                # get CustomerServiceChange
                app_log.info('get CustomerServiceChange data from CDCOSS, so: %s, co: %s'%(query.so, query.co))
                op='CT-COM-XA'
                serialuserid=query.co
                customerid=query.customerid
                name=query.name
                co = query.co
                send_status='0'
                succeed_status='0'
                finish_status = '0'
                last_modify_time = datetime.now()
                errormsg=''
                ordertype='1'
                location=query.location
                servicecode='CustomerServiceChange'
                parameters='address=%s,tel=%s,tariff_id=%s,tariff_n=%s,tariff_p=99'%(query.cust_address, \
                    query.contact_info, query.tariff_id, query.tariff_n)

                if query.cardtype in ['身份证','其他']:
                    cardtype=query.cardtype
                    idcardnum=query.idcardnum
                else:
                    raise ValueError("Invalid cardtype!")
                query_element = session.query(ServiceChange).filter(ServiceChange.serialuserid==query.co
                    ).one_or_none()
                if query_element is None:
                    # query_element = ServiceChange()
                    # merge data to ServiceChange, if data exist, then update, else insert data
                    session.add(ServiceChange(op=op, serialuserid=serialuserid, 
                        customerid=customerid, name=name, cardtype=cardtype, idcardnum=idcardnum, 
                        servicecode=servicecode, location=location, ordertype=ordertype, CO=co, 
                        parameters=parameters,succeed_status=succeed_status, 
                        send_status=send_status, last_modify_time=last_modify_time, errormsg=errormsg,
                        acc_nbr=query.acc_nbr))
                    session.commit()
                app_log.info('write data to ServiceChange, serialuserid: %s, co: %s'%(serialuserid, co))

            #------------------------------------------------------------------------------------------#        
            # other order type
            other_order = session.query(CDCOSS).filter(CDCOSS.columns.co==co_item)
            for query in other_order:
                app_log.info('get %s data from CDCOSS, serialuserid: %s, co: %s'%(query.servicecode, 
                    query.so, query.co))
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
                if query.cardtype in ['身份证','其他']:
                    cardtype=query.cardtype
                    idcardnum=query.idcardnum
                else:
                    raise ValueError("Invalid cardtype!")

                location=query.location
                if query.servicecode=='宽带':
                    servicecode='Internet-Bridge'
                    if query.ordertype=='新装':
                        parameters='UserName=%s,Pwd=%s,DownSpeed=%s' %(query.acc_nbr, query.pwd, \
                            query.downspeed)
                    else:
                        parameters=''
                elif query.servicecode=='网络电视(IPTV)':
                    servicecode='IPTV-Bridg'
                    if query.ordertype=='新装':
                        parameters='UserName=%s,Pwd=%s, CTName=%s,CTPwd=%s' %(query.username, \
                            query.itvpwd, query.username, query.ctname)
                    else:
                        parameters=''
                elif query.servicecode=='普通电话接入':
                    servicecode='VOIP-Route-PPP'
                    if query.ordertype=='新装':
                        parameters = 'SIPUserName=xxx,SIPPassword=xxx' %(query.acc_nbr)
                    else:
                        parameters = ''
                else:
                    raise ValueError("Invalid servicecode!")

                if query.ordertype=='新装':
                    ordertype='1'
                elif query.ordertype=='停机':
                    ordertype='2'
                elif query.ordertype=='复机':
                    ordertype='3'
                elif query.ordertype=='注销产品':
                    ordertype='4'
                elif query.ordertype=='改速率':
                    ordertype='5'
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

            #------------------------------------------------------------------------------------------#        
            # ordertype 4 generate CustomerServiceChange
            new_order = session.query(CDCOSS).filter(CDCOSS.columns.co==co_item, 
                CDCOSS.columns.ordertype=='注销产品')
            if new_order.count()>0:
                query=new_order[0]
                # get CustomerServiceChange
                app_log.info('get CustomerServiceChange data from CDCOSS, so: %s, co: %s'%(query.so, query.co))
                op='CT-COM-XA'
                serialuserid=query.co
                customerid=query.customerid
                name=query.name
                co = query.co
                send_status='0'
                succeed_status='0'
                finish_status = '0'
                last_modify_time = datetime.now()
                errormsg=''
                ordertype='4'
                location=query.location
                servicecode='CustomerServiceChange'
                parameters='address=%s,tel=%s,tariff_id=%s,tariff_n=%s,tariff_p=99'%(query.cust_address, \
                    query.contact_info, query.tariff_id, query.tariff_n)

                if query.cardtype in ['身份证','其他']:
                    cardtype=query.cardtype
                    idcardnum=query.idcardnum
                else:
                    raise ValueError("Invalid cardtype!")
                query_element = session.query(ServiceChange).filter(ServiceChange.serialuserid==query.co
                    ).one_or_none()
                if query_element is None:
                    # query_element = ServiceChange()
                    # merge data to ServiceChange, if data exist, then update, else insert data
                    session.add(ServiceChange(op=op, serialuserid=serialuserid, 
                        customerid=customerid, name=name, cardtype=cardtype, idcardnum=idcardnum, 
                        servicecode=servicecode, location=location, ordertype=ordertype, CO=co, 
                        parameters=parameters,succeed_status=succeed_status, 
                        send_status=send_status, last_modify_time=last_modify_time, errormsg=errormsg,
                        acc_nbr=query.acc_nbr))
                    session.commit()
                app_log.info('write data to ServiceChange, serialuserid: %s, co: %s'%(serialuserid, co))

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
        session.rollback()
        # wait for 1s
        time.sleep(1)
        session.close()

    