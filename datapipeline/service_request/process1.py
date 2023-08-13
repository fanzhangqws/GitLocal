from servicerequest import ServiceRequest
from base import Session, engine, Base
from sqlalchemy import *
import time
from datetime import datetime
import logging
import pandas as pd
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


# global data
faulttype_dict={100002: '宽带故障', 100001:'固话故障', 100004:'IPTV故障'}
df = pd.read_excel('报错大类.xlsx')
keys = list(df['FAULT_PHENOMENA_ID'].values)
values = list([i.split('/')[1] for i in df['大类'].values])
faultdetail_dict=dict(zip(keys, values))

product_id_map = {100002: 42020100, 100001: 42010100, 100004: 23050100}


while True:

  # generate database schema
  Base.metadata.create_all(engine)
  session = Session()
  CDCOSS = Table('changqing_fault', Base.metadata, autoload=True, autoload_with=engine)


  try:
    result_array = []

    for query in session.query(CDCOSS):
      op ='CT-COM-XA'
      serialuserid = query.serialuserid
      name = query.name
      address = query.address
      contact = query.contact
      tel = query.tel
      mobile = query.mobile
      location = query.location
      faulttype = faulttype_dict[query.fault_kind_id]
      customerid = query.cust_id
      faultdetail = faultdetail_dict[query.fault_phenomena_id]
      other = query.other
      acc_nbr = query.acc_nbr
      order_state = query.order_state
      is_that_day = query.is_that_day
      grid_name = query.grid_name
      last_modify_time = datetime.now()
      errormsg = ''
      send_status = '0'
      succeed_status = '0'
      finish_status = '0'
      appl_date = query.first_deal_time

      query_element = session.query(ServiceRequest).filter(ServiceRequest.serialuserid==serialuserid
          ).one_or_none()
      if query_element is None:
        # add data to ServiceChange, if data exist, then update, else insert data
        session.add(ServiceRequest(op=op, serialuserid=serialuserid, 
            customerid=customerid, acc_nbr=acc_nbr, order_state=order_state, is_that_day=is_that_day,
            grid_name=grid_name, name=name, address=address, contact=contact, 
            tel=tel, location=location, mobile=mobile, faulttype=faulttype, appl_date=appl_date,
            faultdetail=faultdetail,succeed_status=succeed_status, other=other,
            send_status=send_status, last_modify_time=last_modify_time, errormsg=errormsg))
        session.commit()
      app_log.info('write data to ServiceRequest, serialuserid: %s'%(serialuserid))

    session.close()        
    # # wait for 5 mins
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
    pass


  