from suds.client import Client  
from Crypto.Cipher import DES
import base64
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import Sequence
import time
import logging
import os 
import datetime
from logging.handlers import RotatingFileHandler
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'




log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = 'process_log/process.log'
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=100, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)
app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

app_log.addHandler(my_handler)



def fetch_data():
    test = Client('http://x.x.x.x:xxxx/DwCCiManvpnUtil/services/DwCCiManvpnUtilService?wsdl')  
    # print (test)  #查看远程方法  
    test.set_options(timeout=180)
    m="{'TOKEN':'xx','ID':'xx','PARAM':{}} "
    crpted_data = test.service.getData(m) #getData为WebService提供的接口 
    return crpted_data

def decrypt_data(crpted_data):
    BS = 8
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
    unpad = lambda s : s[0:-(s[-1])]
    class DESDemo():    
        def __init__(self, key = 'xx'):        
            self.key = key        
            self.mode = DES.MODE_CBC        
        def encrypt(self,text,iv='xxx'):        
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

def update_data(db, data):
    database_query = db.metadata.tables['baixp_data']
    seq = Sequence('order_id_seq')

    stmt = database_query.delete()
    db.session.execute(stmt)
    db.session.commit()

    for item in data:
        stmt = database_query.insert().values(
            单位=item['单位'],
            当前时段值=item['当前时段值'],
            战队=item['战队'],
            序号=item['序号'] if item['序号']!='' else 0,
            今日单卡全拉新=item['今日单卡全拉新'] if item['今日单卡全拉新']!='' else 0,
            橙分期全拉新奋斗目标=item['橙分期全拉新奋斗目标'] if item['橙分期全拉新奋斗目标']!='' else 0,
            当前时段=item['当前时段'] if item['当前时段']!='' else 0,
            今日十点前=item['今日十点前'] if item['今日十点前']!='' else 0,
            今日14至16时=item['今日14至16时'] if item['今日14至16时']!='' else 0,
            今日10至12时=item['今日10至12时'] if item['今日10至12时']!='' else 0,
            今日累计=item['今日累计'] if item['今日累计']!='' else 0,
            橙分期全拉新目标=item['橙分期全拉新目标'] if item['橙分期全拉新目标']!='' else 0,
            今日18至20时=item['今日18至20时'] if item['今日18至20时']!='' else 0,
            今日12至14时=item['今日12至14时'] if item['今日12至14时']!='' else 0,
            有销基数=item['有销基数'] if item['有销基数']!='' else 0,
            今日20至22时=item['今日20至22时'] if item['今日20至22时']!='' else 0,
            有销售门店=item['有销售门店'] if item['有销售门店']!='' else 0,
            今日花呗=item['今日花呗'] if item['今日花呗']!='' else 0,
            今日16至18时=item['今日16至18时'] if item['今日16至18时']!='' else 0,
            昨日同时段累计值=item['昨日同时段累计值'] if item['昨日同时段累计值']!='' else 0,
        )
        db.session.execute(stmt)
    db.session.commit()

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://xx:xx@(DESCRIPTION = \
                        (ADDRESS = \
                        (PROTOCOL = TCP)\
                        (HOST = x.x.x.x)(PORT = xxxx)) (CONNECT_DATA = (SERVER = DEDICATED) \
                        (SERVICE_NAME = jfcrm)))'
db = SQLAlchemy(app)
db.reflect()

while True:
    try:
        crpted_data = fetch_data()
        data = decrypt_data(crpted_data)
        update_data(db, data)
        app_log.info('Updated data!')
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'Updated data!')
        time.sleep(300)

    except Exception as e:
        import traceback
        traceback.print_stack()
        errcode = -1
        errmsg = repr(e)

        # auto-debug based on errmsg
        app_log.error(errmsg)