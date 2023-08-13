from suds.client import Client  
from Crypto.Cipher import DES
import base64
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# 如何添加附件
import os
from sqlalchemy import Sequence
import time
import datetime
import logging
from logging.handlers import RotatingFileHandler
import requests
import random

def fetch_data():
    proxies = {
      "http": "",
      "https": "",
    }
    data = "{'TOKEN':'xx','ID':'xx','PARAM':{}}"
    headers = {'Content-Type':'application/json',
               'X-APP-ID':'xx',
               'X-APP-KEY':'xx',
               'X-CTG-Request-ID':datetime.datetime.now().strftime(
                "%Y%m%d%H%M%S")+str(int(random.random()*10**8))}
    rep = requests.post(
        url='http://xx.xx.xx.xx:xx/DwCCiManvpnUtilRestful/rest/CommonUtilDesService/getDataNew', 
        data=data, headers=headers, proxies = proxies)
    crpted_data = rep.text

    return crpted_data

def decrypt_data(crpted_data, key):
    BS = 8
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
    unpad = lambda s : s[0:-(s[-1])]
    class DESDemo():    
        def __init__(self, key = key):        
            self.key = key        
            self.mode = DES.MODE_CBC        
        def encrypt(self,text,iv='01234567'):        
            cryptor = DES.new(self.key, self.mode, iv)        
            cipher = cryptor.encrypt(pad(text))        
            return cipher.hex()
        def decrypt(self, text,iv):        
            cryptor = DES.new(self.key, self.mode, iv)        
            plain_text = unpad(cryptor.decrypt((text)))        
            return plain_text
    des = DESDemo()
    iv = bytes.fromhex('1234567890abcdef')

    decrpyt_bytes = base64.b64decode(crpted_data)
    result = des.decrypt(decrpyt_bytes,iv)
    result=result.decode('utf8')

    data = eval(result)['DataList']
    return data
    
def update_data2(db, data):
    database_query = db.metadata.tables['eop3']
    seq = Sequence('order_id_seq')

    stmt = database_query.delete()
    db.session.execute(stmt)
    db.session.commit()

    for item in data:
        stmt = database_query.insert().values(
            当前时段值=item['当前时段值'],
            今日单卡全拉新=int(item['今日单卡全拉新']) if item['今日单卡全拉新']!='' else 0,
            橙分期全拉新奋斗目标=int(item['橙分期全拉新奋斗目标']) if item['橙分期全拉新奋斗目标']!='' else 0,
            序号=int(item['序号']) if item['序号']!='' else 0,
            当前时段=int(item['当前时段']) if item['当前时段']!='' else 0,
            今日十点前=int(item['今日十点前']) if item['今日十点前']!='' else 0,
            今日14至16时=int(item['今日14至16时']) if item['今日14至16时']!='' else 0,
            今日10至12时=int(item['今日10至12时']) if item['今日10至12时']!='' else 0,
            今日累计=int(item['今日累计']) if item['今日累计']!='' else 0,
            单位=item['单位'],
            橙分期全拉新目标=int(item['橙分期全拉新目标']) if item['橙分期全拉新目标']!='' else 0,
            今日18至20时=int(item['今日18至20时']) if item['今日18至20时']!='' else 0,
            今日12至14时=int(item['今日12至14时']) if item['今日12至14时']!='' else 0,
            战队=item['战队'],
            有销基数=int(item['有销基数']) if item['有销基数']!='' else 0,
            今日20至22时=int(item['今日20至22时']) if item['今日20至22时']!='' else 0,
            有销售门店=int(item['有销售门店']) if item['有销售门店']!='' else 0,
            今日花呗=int(item['今日花呗']) if item['今日花呗']!='' else 0,
            今日16至18时=int(item['今日16至18时']) if item['今日16至18时']!='' else 0,
            昨日同时段累计值=int(item['昨日同时段累计值']) if item['昨日同时段累计值']!='' else 0,
        )
        db.session.execute(stmt)
    db.session.commit()    
    
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = 'process_log/process3.log'
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=100, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)
app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

app_log.addHandler(my_handler)
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://xx:xxxx@(DESCRIPTION = \
                        (ADDRESS = \
                        (PROTOCOL = TCP)\
                        (HOST = xx.xx.xx.xx)(PORT = xx)) (CONNECT_DATA = (SERVER = DEDICATED) \
                        (SERVICE_NAME = jfcrm)))'
db = SQLAlchemy(app)
db.reflect()

while True:
    try:
        crpted_data2 = fetch_data()
        data2 = decrypt_data(crpted_data2,'xxxx')
        update_data2(db, data2)
        app_log.info('Updated data!')
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S' )+' Updated data!')
        time.sleep(7200)

    except Exception as e:
        import traceback
        traceback.print_stack()
        errcode = -1
        errmsg = repr(e)

        # auto-debug based on errmsg
        app_log.error(errmsg)


