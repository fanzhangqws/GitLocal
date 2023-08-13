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

def fetch_data(num_id, timeout):
    data = "{'TOKEN':'xx','ID':'xx','PARAM':{}}"
    headers = {'Content-Type':'application/json',
               'X-APP-ID':'xx',
               'X-APP-KEY':'xx',
               'X-CTG-Request-ID':datetime.datetime.now(
                ).strftime("%Y%m%d%H%M%S")+str(int(random.random()*10**8))}
    rep = requests.post(
        url='http://xx.xx.xx.xx:xxxx/SCC/capacityRestfulService/api/CfqgetDataNew/CfqgetDataNew', 
        data=data, headers=headers)
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
    database_query = db.metadata.tables['baixp_data2']
    seq = Sequence('order_id_seq')

    stmt = database_query.delete()
    db.session.execute(stmt)
    db.session.commit()

    for item in data:
        stmt = database_query.insert().values(
            积分校验日期=datetime.datetime.strptime(item['积分校验日期'],"%Y-%m-%d %H:%M:%S"),
            sort=item['SORT'],
            发展积分表=item['发展积分表'],
            B级1积分结构=item['B级1积分结构'],
            实体渠道报表=item['实体渠道报表'],
            存量积分表=item['存量积分表'],
            使命报表=item['使命报表'],
            dep=item['DEP'],        
            sor=item['SOR'] if item['SOR']!='' else 0,
            日积分=float(item['日积分']) if item['日积分']!='' else 0,
            周积分=float(item['周积分']) if item['周积分']!='' else 0,
            上周日均积分=float(item['上周日均积分']) if item['上周日均积分']!='' else 0,
            本月累计积分=float(item['本月累计积分']) if item['本月累计积分']!='' else 0,
            上月日均积分=float(item['上月日均积分']) if item['上月日均积分']!='' else 0,
            融合超值积分=float(item['融合超值积分']) if item['融合超值积分']!='' else 0,
            融合高值积分=float(item['融合高值积分']) if item['融合高值积分']!='' else 0,
            融合低值积分=float(item['融合低值积分']) if item['融合低值积分']!='' else 0,
            融合积分合计=float(item['融合积分合计']) if item['融合积分合计']!='' else 0,
            单卡59积分=float(item['单卡59积分']) if item['单卡59积分']!='' else 0,
            单卡59到79积分=float(item['单卡59到79积分']) if item['单卡59到79积分']!='' else 0,
            单卡99积分=float(item['单卡99积分']) if item['单卡99积分']!='' else 0,
            单卡积分合计=float(item['单卡积分合计']) if item['单卡积分合计']!='' else 0,
            实体渠道=float(item['实体渠道']) if item['实体渠道']!='' else 0,
            零销自营厅数=float(item['零销自营厅数']) if item['零销自营厅数']!='' else 0,
            自营厅=float(item['自营厅']) if item['自营厅']!='' else 0,
            自营厅本周日均=float(item['自营厅本周日均']) if item['自营厅本周日均']!='' else 0,
            自营厅上周日均=float(item['自营厅上周日均']) if item['自营厅上周日均']!='' else 0,
            自营厅本月日均 =float(item['自营厅本月日均']) if item['自营厅本月日均']!='' else 0,
            自营厅上月日均=float(item['自营厅上月日均']) if item['自营厅上月日均']!='' else 0,
            社区店总店面数=float(item['社区店总店面数']) if item['社区店总店面数']!='' else 0,
            零销社区店数=float(item['零销社区店数']) if item['零销社区店数']!='' else 0,
            月均零销社区店数=float(item['月均零销社区店数']) if item['月均零销社区店数']!='' else 0,
            小于200分社区店数=float(item['小于200分社区店数']) if item['小于200分社区店数']!='' else 0,
            月均小于200分社区店数=float(item['月均小于200分社区店数']) if item['月均小于200分社区店数']!='' else 0,
            大于等于200分社区店数=float(item['大于等于200分社区店数']) if item['大于等于200分社区店数']!='' else 0,
            月均大于等于200分社区店数=float(item['月均大于等于200分社区店数']) if item['月均大于等于200分社区店数']!='' else 0,
            专营店总店面数=float(item['专营店总店面数']) if item['专营店总店面数']!='' else 0,
            零销专营店数=float(item['零销专营店数']) if item['零销专营店数']!='' else 0,
            月均零销专营店数=float(item['月均零销专营店数']) if item['月均零销专营店数']!='' else 0,
            小于200分专营店数=float(item['小于200分专营店数']) if item['小于200分专营店数']!='' else 0,
            月均小于200分专营店数=float(item['月均小于200分专营店数']) if item['月均小于200分专营店数']!='' else 0,
            大于等于200分专营店数=float(item['大于等于200分专营店数']) if item['大于等于200分专营店数']!='' else 0,
            月均大于等于200分专营店数=float(item['月均大于等于200分专营店数']) if item['月均大于等于200分专营店数']!='' else 0,
            有销本地开放店数=float(item['有销本地开放店数']) if item['有销本地开放店数']!='' else 0,
            本地开放日积分=float(item['本地开放日积分']) if item['本地开放日积分']!='' else 0,
            本地开放月均积分=float(item['本地开放月均积分']) if item['本地开放月均积分']!='' else 0,
            日销售维度积分=float(item['日销售维度积分']) if item['日销售维度积分']!='' else 0,
            日落地维度积分=float(item['日落地维度积分']) if item['日落地维度积分']!='' else 0,
            日合计积分=float(item['日合计积分']) if item['日合计积分']!='' else 0,
            本周日均销售维度积分=float(item['本周日均销售维度积分']) if item['本周日均销售维度积分']!='' else 0,
            本周日均落地维度积分=float(item['本周日均落地维度积分']) if item['本周日均落地维度积分']!='' else 0,
            本周日均合计积分=float(item['本周日均合计积分']) if item['本周日均合计积分']!='' else 0,
            上周日均销售维度积分=float(item['上周日均销售维度积分']) if item['上周日均销售维度积分']!='' else 0,
            上周日均落地维度积分=float(item['上周日均落地维度积分']) if item['上周日均落地维度积分']!='' else 0,
            上周日均合计积分=float(item['上周日均合计积分']) if item['上周日均合计积分']!='' else 0,
            本月日均销售维度积分=float(item['本月日均销售维度积分']) if item['本月日均销售维度积分']!='' else 0,
            本月日均落地维度积分=float(item['本月日均落地维度积分']) if item['本月日均落地维度积分']!='' else 0,
            本月日均合计积分=float(item['本月日均合计积分']) if item['本月日均合计积分']!='' else 0,
            上月日均销售维度积分=float(item['上月日均销售维度积分']) if item['上月日均销售维度积分']!='' else 0,
            上月日均落地维度积分=float(item['上月日均落地维度积分']) if item['上月日均落地维度积分']!='' else 0,
            上月日均合计积分=float(item['上月日均合计积分']) if item['上月日均合计积分']!='' else 0,
            积分大于100分门店占比_销售维度=float(item['积分大于100分门店占比_销售维度']) if item['积分大于100分门店占比_销售维度']!='' else 0,
            积分破0门店占比_销售维度=float(item['积分破0门店占比_销售维度']) if item['积分破0门店占比_销售维度']!='' else 0,
            日目标=float(item['日目标']) if item['日目标']!='' else 0,
            自营厅日完成率=float(item['自营厅日完成率']) if item['自营厅日完成率']!='' else 0,
            自营厅周日均环比=float(item['自营厅周日均环比']) if item['自营厅周日均环比']!='' else 0,
            战区日完成率=float(item['战区日完成率']) if item['战区日完成率']!='' else 0,
            战区日均环比=float(item['战区日均环比']) if item['战区日均环比']!='' else 0,
            商圈日完成率=float(item['商圈日完成率']) if item['商圈日完成率']!='' else 0,
            商圈日均环比=float(item['商圈日均环比']) if item['商圈日均环比']!='' else 0,
            政企日完成率=float(item['政企日完成率']) if item['政企日完成率']!='' else 0,        
            政企周日均环比=float(item['政企周日均环比']) if item['政企周日均环比']!='' else 0,        
            商客日完成率=float(item['商客日完成率']) if item['商客日完成率']!='' else 0,
            商客周日均环比=float(item['商客周日均环比']) if item['商客周日均环比']!='' else 0,
            校园日完成率=float(item['校园日完成率']) if item['校园日完成率']!='' else 0,
            校园周日均环比=float(item['校园周日均环比']) if item['校园周日均环比']!='' else 0,
            xh=float(item['XH']) if item['XH']!='' else 0,
            fzj=float(item['FZJ']) if item['FZJ']!='' else 0,
            ydj=float(item['YDJ']) if item['YDJ']!='' else 0,
            kdj=float(item['KDJ']) if item['KDJ']!='' else 0,
            tvj=float(item['TVJ']) if item['TVJ']!='' else 0,
        )
        db.session.execute(stmt)
    db.session.commit()    
    
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = 'process_log/process2.log'
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
                        (HOST = xx.xx.xx.xx)(PORT = xxxx)) (CONNECT_DATA = (SERVER = DEDICATED) \
                        (SERVICE_NAME = jfcrm)))'
db = SQLAlchemy(app)
db.reflect()

while True:
    try:
        crpted_data2 = fetch_data('xx',timeout=240)
        data2 = decrypt_data(crpted_data2,'xxx')
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


