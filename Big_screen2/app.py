from flask import Flask, request, render_template, jsonify, Blueprint, current_app,session,abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Sequence, Table, func
import flask, os, datetime
from flask_login import (LoginManager, login_user, logout_user, 
    login_required, current_user, UserMixin)
from flask_principal import Principal, Identity, AnonymousIdentity, identity_changed
import numpy as np
import pandas as pd
import requests
import datetime

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://xxx:xxx@(DESCRIPTION =\
                        (ADDRESS = \
                        (PROTOCOL = TCP)\
                        (HOST = x.x.x.x)(PORT = x)) (CONNECT_DATA=(SERVER = DEDICATED)\
                        (SERVICE_NAME = jfcrm)))'
app.config['APPLICATION_ROOT'] = '/bigscreen_kj'
db = SQLAlchemy(app)
db.reflect()

bp = Blueprint('bigscreen_kj', __name__, template_folder='templates',
               static_folder='static')

@bp.route('/main', methods=['GET'])
def main():
    return render_template('main.html')

# @bp.route('/page0', methods=['GET'])
# def get_page0():
#     req_param = request.args.get("image_key")
#     return render_template('index6.html', req_param=req_param)

@bp.route('/page0', methods=['GET'])
def get_page0():
     return render_template('index6.html')

@bp.route('/page01', methods=['GET'])
def get_page01():
    req_param = request.args.get("image_key")
    return render_template('index7.html', req_param=req_param)


@bp.route('/slide_zero', methods=['GET'])
def get_count0():
    future = datetime.datetime(2020,1,1,10,20,30)
    #当前时间
    now = datetime.datetime.now()
    #求时间差
    delta = future - now
    # print("今天是：",print_now)
    # print("距离 2020-01-01 \"work\" 还剩下：%d天"%delta.days)
    json = {'result': delta.days}     
    return jsonify(json)

@bp.route('/page1', methods=['GET'])
def get_page():
     return render_template('index.html')


def fetch_data(serial_no="\"\"", query_date="\"\""):
    data = '{"region_id": 290, "serial_no": %s, "query_date": %s}'%(serial_no, query_date)
    headers = {'Content-Type':'application/json'}
    rep = requests.post(url='http://x.x.x.x:x/OutcryWeb/interface/queryExeStaReport',
        data=data, headers=headers) 
    return eval(rep.text)

def fetch_data2(serial_no):
    data = '{"region_id": 290, "serial_no": %s}'%(serial_no)
    headers = {'Content-Type':'application/json'}
    rep = requests.post(url='http://x.x.x.x:x/OutcryWeb/interface/queryAccStaReport', 
        data=data, headers=headers) 
    return eval(rep.text)

def fetch_data3(serial_no):
    data = '{"region_id": 290, "serial_no": %s}'%(serial_no)
    headers = {'Content-Type':'application/json'}
    rep = requests.post(url='http://x.x.x.x:x/OutcryWeb/interface/queryRealTimeMonitor',
        data=data, headers=headers) 
    return eval(rep.text)

def statics_result(rec_data):
    # 截止时间
    year=rec_data['report_date'].split(' ')[0].split('-')[0]
    month=rec_data['report_date'].split(' ')[0].split('-')[1]
    day=rec_data['report_date'].split(' ')[0].split('-')[2]
    hour = rec_data['report_date'].split(' ')[1].split(':')[0]
    minutes=rec_data['report_date'].split(' ')[1].split(':')[1]
    # 执行工单量
    total_executed_count=0
    # 呼通工单量
    total_call_count=0
    # 有效外呼量
    total_effcall_count=0
    # 营销成功量
    total_exe_success_count=0
    # 受理成功量
    total_accept_count=0
    # 驳回工单量
    total_reject_count=0
    # 未受理工单量
    total_unaccept_count=0
    for item in rec_data['project_report']:
        if item['group_name'] in ['存量营销一部', '存量营销二部']:
            total_executed_count+=item['executed_count']
            total_call_count+=item['call_count']
            total_effcall_count+=item['effcall_count']
            total_exe_success_count+=item['exe_success_count']
            total_accept_count+=item['accept_count']
            total_reject_count+=item['reject_count']
            total_unaccept_count+=item['unaccept_count']
        # 接通率
    rate1 = round(100*total_call_count/(total_executed_count+1e-9),0)
    rate1 = rate1 if rate1<100 else 100
    # 营销成功率
    rate2 = round(100*total_exe_success_count/(total_call_count+1e-9),0)
    rate2 = rate2 if rate2<100 else 100

    return year,month,day,hour,minutes,total_executed_count,\
        total_call_count,total_effcall_count,total_exe_success_count,\
        total_accept_count,rate1,rate2,total_reject_count,total_unaccept_count

# slide one data
@bp.route('/slide_one', methods=['GET'])
def get_count():
    date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    rec_data = fetch_data(date)
    # --------------------------营销快报模块---------------------------------------------------
    year,month,day,hour,minutes,total_executed_count,total_call_count,\
    total_effcall_count,total_exe_success_count,total_accept_count,_,_,_,_=statics_result(rec_data)
    # -------------------------------外呼人员参与度模块----------------------------------------
    effcall_num1=0
    total_num1=0
    effcall_num2=0
    total_num2=0
    for item in rec_data['project_report']:
        if item['group_name']=='存量营销一部':
            total_num1+=1
            if item['effcall_count']>0:
                effcall_num1+=1
        if item['group_name']=='存量营销二部':
            total_num2+=1
            if item['effcall_count']>0:
                effcall_num2+=1
    rate1=round(100*effcall_num1/(total_num1+1e-9),0)
    rate2=round(100*effcall_num2/(total_num2+1e-9),0)
    rate1 = rate1 if rate1<100 else 100
    rate2 = rate2 if rate2<100 else 100
    # -------------------------------工单执行总量,营销成功及受理量-------------------------------
    past_total_executed_count=[]
    past_total_exe_success_count=[]
    past_total_accept_count=[]
    past_date=[]
    for i in range(-6,1):
        date = (datetime.datetime.now()+datetime.timedelta(days=i)).strftime('%Y%m%d')
        
        if i==0:
            rec_data = fetch_data(datetime.datetime.now().strftime('%Y%m%d%H%M%S'),"\"\"")
        else:
            rec_data = fetch_data(_,date)
        _,_,_,_,_,total_executed_count,_,_,total_exe_success_count,\
        total_accept_count,_,_,_,_=statics_result(rec_data)
        past_total_executed_count.append(total_executed_count)
        past_total_exe_success_count.append(total_exe_success_count)
        past_total_accept_count.append(total_accept_count)
        past_date.append((datetime.datetime.now()+datetime.timedelta(days=i)
            ).strftime('%m{m}%d{d}').format(m='月', d='日'))

    json = {'part1': [year,month,day,hour,minutes,total_executed_count,total_call_count,
    total_effcall_count,total_exe_success_count,total_accept_count], 
    'part2': [rate1,rate2],'part3':[past_date,past_total_executed_count],
    'part4':[past_date,past_total_exe_success_count,past_total_accept_count]}     
    return jsonify(json)

@bp.route('/page2', methods=['GET'])
def index2():
    return render_template('index2.html')

@bp.route('/slide_two', methods=['GET'])
def get_count2():
    date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    rec_data = fetch_data(date)
    df = pd.DataFrame(rec_data['project_report'])
    # -----------------------------------top bar -----------------------------------------
    _,_,_,hour,minutes,total_executed_count,total_call_count,\
    total_effcall_count,total_exe_success_count,total_accept_count,\
    rate1,rate2,_,_=statics_result(rec_data)
    # -----------------------------------left multi bar chart-----------------------------
    df2 = df[df['group_name'].isin(['存量营销一部', '存量营销二部'])]
    df3 = df2.groupby('campaign_name').sum()
    df3['assigned_count'] = df2.groupby(['campaign_name','class_name']).max(
        ).reset_index().groupby('campaign_name').sum()['assigned_count']

    df3.sort_values(by=['exe_success_count'], ascending=False, inplace=True)
    df3 = df3.head(5)

    campaign_name = list(df3.index.values[::-1])
    accept_count_list = [int(x) for x in df3['exe_success_count'].values[::-1]]
    exe_success_count_list = [int(x) for x in df3['exe_success_count'].values[::-1]]
    executed_count_list = [int(x) for x in df3['executed_count'].values[::-1]]
    assigned_count_list = [int(x) for x in df3['assigned_count'].values[::-1]]   
    # -----------------------------------right multi bar chart-----------------------------
    df4 = df2.groupby(['class_name']).sum()
    class_name = ['营销一班', '营销二班', '营销三班', '营销四班', '营销五班', '营销六班',
     '营销七班', '营销八班', '营销实验班']
    call_count_list = [int(x) for x in df4.loc[class_name,'call_count'].fillna(0).values]
    effcall_count_list = [int(x) for x in df4.loc[class_name,'effcall_count'].fillna(0).values]
    avg_eff_count = effcall_count_list # TODO

    json = {
        'left_table_data': [campaign_name, accept_count_list, exe_success_count_list, 
            executed_count_list, assigned_count_list],
        'right_table_data': [class_name,call_count_list, effcall_count_list, avg_eff_count],
        'top_table_data': [hour,minutes,total_executed_count,
            total_call_count,rate1,total_effcall_count,rate2,total_accept_count]
        }
    # print(json)
    return jsonify(json)



@bp.route('/page3', methods=['GET'])
def index3():
    return render_template('index3.html')

@bp.route('/slide_three', methods=['GET'])
def get_count3():
    date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    rec_data = fetch_data(date)
    df = pd.DataFrame(rec_data['project_report'])
    # -----------------------------------top bar -----------------------------------------
    _,_,_,hour,minutes,total_executed_count,total_call_count,total_effcall_count,\
    total_exe_success_count,total_accept_count,rate1,rate2,_,_=statics_result(rec_data)
    # -----------------------------------left multi bar chart-----------------------------
    df = pd.DataFrame(rec_data['project_report'])
    df2 = df[df['group_name'].isin(['存量营销一部', '存量营销二部'])]
    df4 = df2.groupby(['class_name']).sum()
    class_name = ['营销一班', '营销二班', '营销三班', '营销四班', '营销五班', '营销六班',
     '营销七班', '营销八班', '营销实验班']
    executed_count_list=[int(x) for x in df4.loc[class_name,'executed_count'].fillna(0).values]
    call_count_list = [int(x) for x in df4.loc[class_name,'call_count'].fillna(0).values]
    success_rate_list = list((df4.loc[class_name,'exe_success_count'].fillna(0)/(
        df4.loc[class_name,'call_count'].fillna(0)+1e-9)).map(
        lambda x: round(x*100,2) if round(x*100,2)<100 else 100).values)
    success_count_list = [int(x) for x in df4.loc[class_name,'exe_success_count'].fillna(0).values]
    # -----------------------------------right table chart-------------------------------
    df2['rate'] = (df2['exe_success_count']/(df2['executed_count']+1e-9)
        ).map(lambda x: str(round(x*100,2) if round(x*100,2)<100 else 100)+'%')
    df3=df2[df2['user_name']!='']
    df5 = df3[['user_name','class_name','executed_count','call_count','exe_success_count','rate'
          ]].sort_values(by=['exe_success_count','rate'], ascending=False)
    df6 = df5.head(15)
    # result = list(df6.T.to_dict().values())
    result = df6.values.tolist()

    json = {'left_table_data': [class_name,executed_count_list, call_count_list, 
        success_rate_list,success_count_list], 'right_table_data': result,
        'top_table_data': [hour,minutes,total_executed_count,
            total_call_count,rate1,total_effcall_count,rate2,total_accept_count]}
    return jsonify(json)


@bp.route('/page4', methods=['GET'])
def index4():
    return render_template('index4.html')

@bp.route('/slide_four', methods=['GET'])
def get_count4():
    date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    rec_data = fetch_data(date)
    # -----------------------------------top bar -----------------------------------------
    _,_,_,hour,minutes,total_executed_count,total_call_count,total_effcall_count,\
    total_exe_success_count,total_accept_count,rate1,rate2,_,_=statics_result(rec_data)
    # -----------------------------------left multi bar chart-----------------------------
    rec_data2 = fetch_data3(date)
    df = pd.DataFrame(rec_data2['call_report'])
    df2 = df[df['group_name'].isin(['存量营销一部', '存量营销二部'])]
    class_list = ['营销一班', '营销二班', '营销三班', '营销四班', '营销五班', '营销六班',
     '营销七班', '营销八班', '营销实验班']
    state1_count=[]
    state2_count=[]
    state3_count=[]
    for i in class_list:
        state1_count.append(len(df2[(df2['class_name']==i) & (df2['state']=='1')]))
        state2_count.append(len(df2[(df2['class_name']==i) & (df2['state']=='2')]))
        state3_count.append(len(df2[(df2['class_name']==i) & (df2['state']=='3')]))

    state0_count = [int(i) for i in list(np.array(state1_count)+
        np.array(state2_count)+np.array(state3_count))]
    # -----------------------------------right table chart-------------------------------
    df = pd.DataFrame(rec_data['project_report'])
    df2 = df[df['group_name'].isin(['存量营销一部', '存量营销二部'])]
    df3=df2[df2['user_name']!='']
    df5 = df3[['user_name','class_name','call_count','effcall_count'
          ]].sort_values(by=['effcall_count'], ascending=False).head(15)
    # result = list(df5.T.to_dict().values())
    result = df5.values.tolist()
    # for i in range(len(result[0])):
    #     item['call_count'] = int(item['call_count'])
    #     item['effcall_count'] = int(item['effcall_count'])
    for i in range(len(result)):
        result[i][2] = int(result[i][2])
        result[i][3] = int(result[i][3])

    json = {'left_table_data': [class_list,state0_count, state1_count, state2_count,
        state3_count], 'right_table_data': result,
        'top_table_data': [hour,minutes,total_executed_count,
            total_call_count,rate1,total_effcall_count,rate2,total_accept_count]}
    return jsonify(json)

@bp.route('/page5', methods=['GET'])
def index5():
    return render_template('index5.html')

@bp.route('/slide_five', methods=['GET'])
def get_count5():
    date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    rec_data = fetch_data(date)
    # -----------------------------------top bar -----------------------------------------
    _,_,_,hour,minutes,total_executed_count,total_call_count,total_effcall_count,\
    total_exe_success_count,total_accept_count,rate1,rate2,_,_=statics_result(rec_data)
    # -----------------------------------left multi bar chart-----------------------------
    rec_data2 = fetch_data2(date)
    df = pd.DataFrame(rec_data2['accept_report'])
    df2 = df[df['group_name'].isin(['营销支撑部'])]
    df3 = df2.groupby('bus_type').sum().sort_values(
        by=['accept_count'], ascending=False)['accept_count']
    y_index = list(df3.index.values[::-1])
    x_values = [int(x) for x in list(df3.values[::-1])]
    # -----------------------------------right table chart-------------------------------
    df4=df2[df2['user_name']!='']
    df5 = df4.groupby('user_name').sum(
        )[['accept_count','reject_count']].sort_values(by=['accept_count'], 
        ascending=False).head(22)
    # result = list(df5.T.to_dict().values())
    result = df5.reset_index().values.tolist()
    # for i in range(len(result)):
    #     item=result[i]
    #     item['accept_count'] = int(item['accept_count'])
    #     item['reject_count'] = int(item['reject_count'])
    #     item['user_name'] = list(df5.index)[i]

    for i in range(len(result)):
        result[i][2] = int(result[i][2])
        result[i][1] = int(result[i][1])

    #-----------------------------------right bot bar chart-------------------------------
    past_total_executed_count=[]
    past_total_order_count=[]
    past_total_accept_count=[]
    past_date=[]
    rate3_list =[]
    for i in range(-6,1):
        date = (datetime.datetime.now()+datetime.timedelta(days=i)).strftime('%Y%m%d')
        
        if i==0:
            rec_data = fetch_data(datetime.datetime.now().strftime('%Y%m%d%H%M%S'),"\"\"")
        else:
            rec_data = fetch_data(_,date)
        _,_,_,_,_,total_executed_count,_,_,total_exe_success_count,\
        total_accept_count,_,_,total_reject_count,total_unaccept_count=statics_result(rec_data)

        past_total_order=total_accept_count+total_reject_count+total_unaccept_count
        past_total_order_count.append(past_total_order)
        past_total_accept_count.append(total_accept_count)
        rate3=round(100*total_accept_count/(past_total_order+1e-9),0)
        rate3 = rate3 if rate3<100 else 100
        rate3_list.append(rate3)
        past_date.append((datetime.datetime.now()+datetime.timedelta(days=i)
            ).strftime('%m{m}%d{d}').format(m='月', d='日'))

    
    print(past_total_order_count,past_total_accept_count,rate3_list)


    json = {'left_table_data': [y_index,x_values], 'right_table_data': result,
            'top_table_data': [hour,minutes,total_executed_count,
            total_call_count,rate1,total_effcall_count,rate2,total_accept_count],
            'right_bot_data':[past_date,past_total_accept_count, 
            past_total_order_count, rate3_list]}
    return jsonify(json)


@bp.route('/upload')
def upload():
    return render_template('upload.html')

@bp.route('/input_data', methods=['POST'])
def input_data():
    errcode = 0
    errmsg = ''
    file_name = request.files['importfile']
    df_blank = pd.read_excel(file_name)
    df = df_blank.dropna(how='all')
    seq = Sequence('order_id_seq')
    user_group_table = db.metadata.tables['user_group_table']
    try:
        stmt = user_group_table.delete()
        db.session.execute(stmt)
        for i in df.index:
            row_content = df.loc[i]
            # print(row_content.user_name)
            stmt = user_group_table.insert().values(
                row_id=seq.next_value(),
                user_name=row_content.user_name,
                user_group=row_content.user_group,
                user_id=row_content.user_id
                )
            db.session.execute(stmt)

        db.session.commit()
        errmsg = '上传成功!'
    except Exception as e:
        import traceback
        traceback.print_stack()
        errcode = -1
        errmsg = repr(e)
        raise e

    return jsonify({"errcode": errcode, "errmsg": errmsg})


app.register_blueprint(bp, url_prefix='/bigscreen_kj')


def main():
    app.run(host='127.0.0.1', port='8000', debug=True)


if __name__ == '__main__':
    main()
