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
    burp0_url = "http://133.64.98.75:9970/sps/nwo/tneticket/dummy/searchSolr.json?search=true&qryFlag=maintain"
    # finish order
    burp1_url = "http://133.64.98.75:9970/sps/nwo/tneticket/dummy/returnNAException4Wo"
    burp0_cookies = {" rememberMe": "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"}
    burp0_headers = {"x-requested-with": "XMLHttpRequest", "Accept-Language": "zh-CN", "Referer": "http://133.64.98.75:9970/sps/nwo/tneticket", "Accept": "application/json, text/javascript, */*; q=0.01", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Accept-Encoding": "gzip, deflate", "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)", "Pragma": "no-cache", "Connection": "close"}
    burp1_headers = {"POST http": "/133.64.98.75:9970/sps/nwo/tneticket/dummy/returnNAException4Wo HTTP/1.1", "x-requested-with": "XMLHttpRequest", "Accept-Language": "zh-CN", "Referer": "http://133.64.98.75:9970/sps/nwo/tneticket/dummy/initReturnNA4Wo", "Accept": "application/json, text/javascript, */*; q=0.01", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Accept-Encoding": "gzip, deflate", "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)", "Pragma": "no-cache", "Connection": "close"}

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
