# -*- coding: utf-8 -*-
from servicechange import ServiceChange
from base import Session, engine, Base
from sqlalchemy import *
import time
import requests
import logging
import urllib
import os 
from logging.handlers import RotatingFileHandler
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'




log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = 'process_log/process3.log'
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
    # search order
    burp0_url = "http://x.x.x.x:xxxx/sps/nwo/tneticket/dummy/searchSolr.json?search=true&qryFlag=maintain"
    # finish order
    burp1_url = "http://x.x.x.x:xxxx/sps/nwo/tneticket/dummy/returnNAException4Wo"
    burp0_cookies = {" rememberMe": "xxxx"}
    burp0_headers = {"x-requested-with": "XMLHttpRequest", "Accept-Language": "zh-CN", "Referer": "http://x.x.x.x:xxxx/sps/nwo/tneticket", "Accept": "application/json, text/javascript, */*; q=0.01", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Accept-Encoding": "gzip, deflate", "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)", "Pragma": "no-cache", "Connection": "close"}
    burp1_headers = {"POST http": "/x.x.x.x:xxxx/sps/nwo/tneticket/dummy/returnNAException4Wo HTTP/1.1", "x-requested-with": "XMLHttpRequest", "Accept-Language": "zh-CN", "Referer": "http://x.x.x.x:xxxx/sps/nwo/tneticket/dummy/initReturnNA4Wo", "Accept": "application/json, text/javascript, */*; q=0.01", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Accept-Encoding": "gzip, deflate", "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)", "Pragma": "no-cache", "Connection": "close"}

    try:
        # get SO list
        so_list = []
        for query in session.query(ServiceChange):
            if query.serialuserid not in so_list:
                so_list.append(query.serialuserid)

        # request available unfinished orders for each so            
        for so in so_list:

            app_log.info('request available unfinished orders for so : %s '%(so))

            burp0_data={"alarm": '', "vcwid": so, "vcsvcareaid": "4A_401000", "page": "1", "rp": "50", "usePager": "true", "sortFlag": "1&"}
            r = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
            data = r.json()

            # each so may contains more than one unfinished orders
            for raw_data in data['rows']:

                app_log.info('post unfinished order with soNbr : %s and woNbr : %s'%(raw_data['VCWID'], raw_data['VCSUBWID']))

                burp1_data={"soNbr": raw_data['VCWID'], "woNbr": raw_data['VCSUBWID'], "sourceid": raw_data['ISOURCEID'], "neticketid": raw_data['VCNETICKETID'], "realtimeflag": "Y", "returnFlag": "success", "remarks": "长庆光改", "errCode": "0", "shardingId": raw_data['SHARDING_ID'], "vcBackInfo": urllib.parse.quote_plus(raw_data['VCBACKINFO'], encoding='utf8')}
                requests.post(burp1_url, headers=burp1_headers, cookies=burp0_cookies, data=burp1_data)                

                app_log.info('unfinished order with soNbr : %s and woNbr : %s is finished!'%(raw_data['VCWID'], raw_data['VCSUBWID']))

        session.close()
        # wait for 12 hours
        t_duration = 3600*12
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
