from flask import Flask, request, render_template, jsonify, Blueprint, current_app, session, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Sequence, Table, func
import flask, os, datetime
from flask_login import (LoginManager, login_user, logout_user, 
    login_required, current_user, UserMixin)
from flask_principal import Principal, Identity, AnonymousIdentity, identity_changed
import numpy as np
import pandas as pd

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://xxxx:xxxx@(DESCRIPTION = \
                        (ADDRESS = \
                        (PROTOCOL = TCP)\
                        (HOST = x.x.x.x)(PORT = xxxx)) (CONNECT_DATA = (SERVER = DEDICATED) \
                        (SERVICE_NAME = jfcrm)))'
app.config['APPLICATION_ROOT'] = '/bigscreen'
db = SQLAlchemy(app)
db.reflect()

# db.engine.execute("call proc_order_score('20190703')")

bp = Blueprint('bigscreen', __name__, template_folder='templates',
               static_folder='static')

@bp.route('/main', methods=['GET'])
def main():
    return render_template('main.html')


@bp.route('/page1/<agent>', methods=['GET'])
def get_page(agent):
     return render_template('common_index.html', agent=agent)

# slide one data
@bp.route('/slide_one', methods=['GET'])
def get_count():
    dic = {
        '1': '中意',
        '2': '同步伟业',
        '3': '智凌'
    }
    agent = request.args.get('agent')
    if agent is None:
        abort(400)

    goal = 175
    group_name = dic[agent]
    total_table = db.metadata.tables['ljn_xbd_190528_yz_04']
    user_group_table = db.metadata.tables['user_group_table']
    people_list_all = db.session.query(user_group_table.c.user_name).filter(
        user_group_table.c.user_group==group_name).all()
    people_list=[]
    for item in people_list_all:
        people_list.append(item[0])
    print(people_list)
    # find available people list
    selected_query_people = db.session.query(total_table.c.中台接单人, 
        func.count(total_table.c.中台接单人)
        ).filter(total_table.c.中台接单人.in_(people_list),total_table.c.积分!=None, 
        total_table.c.工单状态描述.in_(['已处理','已取消'])
        ).group_by(total_table.c.中台接单人).all()
    print(selected_query_people)

    test_list = []
    for i in people_list:
        print(i,'高婵')
        temp = db.session.query(total_table.c.中台接单人, 
        func.count(total_table.c.中台接单人)
        ).filter(total_table.c.中台接单人==i,total_table.c.积分!=None, 
        total_table.c.工单状态描述.in_(['已处理','已取消'])
        ).group_by(total_table.c.中台接单人).all()
        print(temp)
        # if temp is not None:
        #     test_list.append(temp[0])
    # print(test_list)
    y_data=[]
    for raw in selected_query_people:
        y_data.append(raw[0])
    # get table data
    selected_query = db.session.query(total_table.c.中台接单人, total_table.c.积分, 
        func.count(total_table.c.积分)
        ).filter(total_table.c.中台接单人.in_(people_list),total_table.c.积分!=None, 
        total_table.c.工单状态描述.in_(['已处理','已取消'])
        ).group_by(total_table.c.中台接单人, total_table.c.积分).all()
    # print(selected_query)
    table_data = np.zeros((len(y_data),5))
    
    for item in selected_query:
        if item[1] == '5':
            x_index = 1
        elif item[1] == '3':
            x_index = 2
        else:
            x_index = 3
        y_index = y_data.index(item[0])
        table_data[y_index, x_index] = item[2]
    table_data[:,4] = table_data[:,1]*5+table_data[:,2]*3+table_data[:,3]
    total_point=np.sum(table_data[:,4])
    list_data = []
    for i in range(len(table_data)):
        temp = {'t0': y_data[i], 't1': int(table_data[i,1]), 't2': int(table_data[i,2]),
         't3': int(table_data[i,3]), 't4': int(table_data[i,4]), 
         't5': int(table_data[i,1])+int(table_data[i,2])+int(table_data[i,3])}
        list_data.append(temp)

    # # get bar chart data
    cum_achieve= []
    cum_diff = []
    cum_addition = []
    achieve_percent=[]
    total_order=0
    for raw in table_data:
        total_order+=sum(raw[:4])
        achieve_percent.append(str(int(100*raw[4]/goal))+'%')
        if raw[4]<goal:
            cum_achieve.append(raw[4])
            cum_diff.append(goal-raw[4])
            cum_addition.append(0)
        elif raw[4]==goal:
            cum_achieve.append(raw[4])
            cum_diff.append(0)
            cum_addition.append(0)
        else:
            cum_achieve.append(goal)
            cum_diff.append(0)
            cum_addition.append(raw[4]-goal)

    json = {'querys': [y_data[::-1], cum_achieve[::-1], cum_diff[::-1],
    cum_addition[::-1], achieve_percent[::-1]],
    'list_data': list_data,'group_name':group_name,
    'total_order':total_order,'total_point':total_point}
    return jsonify(json)

@bp.route('/page2', methods=['GET'])
def index2():
    return render_template('index2.html')

@bp.route('/slide_two', methods=['GET'])
def get_count2():
    # left bar chart
    table_shuaidan = db.engine.execute("select 渠道, count(*) as 甩单 from \
        (select y.*, x.渠道主管部门 渠道 from yangchen.yc_sort_channel@jfcrm x,\
         ljn_xbd_190528_yz y,\
        ywxt.mv_crm_org@jfcrm  t where t.org_id=y.sel_In_org_id and x.销售点编码=t.org_jt_code \
          and 渠道主管部门 in ('营业部','社区运营部','商业客户部') ) group by 渠道")
    product_list = ['product','营业厅','社区专营店','政企业务']
    first_column=['甩单量',0,0,0]
    for item in table_shuaidan:
        if item[0]=='营业部':
            first_column[1]=item[1]
        elif item[0]=='社区运营部':
            first_column[2]=item[1]
        elif item[0]=='商业客户部':
            first_column[3]=item[1]
    total_order = sum(first_column[1:])

    table_achieve = db.engine.execute("select 渠道, count(*) as 已完成 from \
        ( select y.*, x.渠道主管部门 渠道 from yangchen.yc_sort_channel@jfcrm x, \
        ljn_xbd_190528_yz y,\
        ywxt.mv_crm_org@jfcrm  t where t.org_id=y.sel_In_org_id and x.销售点编码=t.org_jt_code \
          and 渠道主管部门 in ('营业部','社区运营部','商业客户部') and \
          (y.工单状态描述 in ('已处理', '已取消'))\
        ) group by 渠道")
    second_column = ['已完成',0,0,0]
    for item in table_achieve:
        if item[0]=='营业部':
            second_column[1]=item[1]
        elif item[0]=='社区运营部':
            second_column[2]=item[1]
        elif item[0]=='商业客户部':
            second_column[3]=item[1]
    total_achieve = sum(second_column[1:])

    table_not_achieve = db.engine.execute("select 渠道, count(*) as 未完成 from \
        (select y.*, x.渠道主管部门 渠道 from yangchen.yc_sort_channel@jfcrm x, \
        ljn_xbd_190528_yz y,\
        ywxt.mv_crm_org@jfcrm  t where t.org_id=y.sel_In_org_id and \
        x.销售点编码=t.org_jt_code and \
        渠道主管部门 in ('营业部','社区运营部','商业客户部') and \
        (y.工单状态描述 is null or y.工单状态描述='待确认')\
        ) group by 渠道")
    third_column = ['未完成',0,0,0]
    for item in table_not_achieve:
        if item[0]=='营业部':
            third_column[1]=item[1]
        elif item[0]=='社区运营部':
            third_column[2]=item[1]
        elif item[0]=='商业客户部':
            third_column[3]=item[1]



    # -----------------------------------right stack bar chart-----------------------------
    incomplete_list = [0]*6
    overtime_list = [0]*6

    # 非时效 已超时
    no_time_order_overtime = db.engine.execute("select 渠道, count(*) as 甩单  from \
        (select * from v_no_time_order where (工单状态描述 is null  or 工单状态描述='待确认')\
        and 渠道 in ('社区运营部','营业部') and  (SYSDATE - create_date) > 10/60/24\
        ) group by 渠道")

    for item in no_time_order_overtime:
        if item[0]=='营业部':
            overtime_list[0]=item[1]
        if item[0]=='社区运营部':
            overtime_list[2]=item[1]

    # 时效 已超时
    time_order_wait_overtime = db.engine.execute("select 渠道, count(*) as 甩单  from \
        (select * from v_time_order where (工单状态描述 is null  or 工单状态描述='待确认')\
         and 渠道 in ('社区运营部','营业部') and  (SYSDATE - create_date) > 10/60/24\
        ) group by 渠道")

    for item in time_order_wait_overtime:
        if item[0]=='营业部':
            overtime_list[1]=item[1]
        if item[0]=='社区运营部':
            overtime_list[3]=item[1]

    # 非时效 未完成
    no_time_order_incomplete = db.engine.execute("select 渠道, count(*) as 甩单 from \
        (select * from v_no_time_order where (工单状态描述 is null  or 工单状态描述='待确认')\
         and 渠道 in ('社区运营部','营业部'))group by 渠道")

    for item in no_time_order_incomplete:
        if item[0]=='营业部':
            incomplete_list[0]=item[1]-overtime_list[0]
        if item[0]=='社区运营部':
            incomplete_list[2]=item[1]-overtime_list[2]

    # 时效 未完成
    time_order_incomplete = db.engine.execute("select 渠道, count(*) as 甩单 from \
        (select * from v_time_order where (工单状态描述 is null \
         or 工单状态描述='待确认') and 渠道 in ('社区运营部','营业部'))\
        group by 渠道")

    for item in time_order_incomplete:
        if item[0]=='营业部':
            incomplete_list[1]=item[1]-overtime_list[1]
        if item[0]=='社区运营部':
            incomplete_list[3]=item[1]-overtime_list[3]

    json = {
        'left_table_data': [product_list, first_column, second_column, third_column],
        'incomplete_list': incomplete_list,
        'overtime_list': overtime_list,
        'total_order':total_order,
        'total_achieve':total_achieve
        }
    return jsonify(json)



@bp.route('/page3', methods=['GET'])
def index3():
    return render_template('index3.html')

@bp.route('/slide_three', methods=['GET'])
def get_count3():
    # overtime alert static
    total_table_static = Table('t_time_order_static', 
        db.metadata, autoload=True, autoload_with=db.engine)
    # total_table = db.metadata.tables['v_time_order_count']
    data = db.session.query(total_table_static.c.count_num).all()
    result = []
    for i in data:
        result.append(i[0])

    # overtime alert realtime
    total_table = Table('v_time_order_count', db.metadata, autoload=True, autoload_with=db.engine)
    # total_table = db.metadata.tables['v_time_order_count']
    data = db.session.query(total_table.c.count_num).all()
    result1 = []
    for i in data:
        result1.append(i[0])
    total_realsum = sum(result1)

    # total order
    total_table2 = Table('v_time_order_sum', db.metadata, autoload=True, autoload_with=db.engine)
    data2 = db.session.query(total_table2.c.count_num).all()
    result2 = []
    for i in data2:
        result2.append(i[0])

    # pos = np.argwhere(np.array(result2)>0)[-1][0]
    # result2[:pos+1] = np.cumsum(result2[:pos+1])

    json = {'result':result, 'result2':result2, 'total_realsum':total_realsum}
    return jsonify(json)


@bp.route('/page4', methods=['GET'])
def index4():
    return render_template('index4.html')

@bp.route('/slide_four', methods=['GET'])
def get_count4():
    # overtime alert static
    total_table_static = Table('t_no_time_order_static', 
        db.metadata, autoload=True, autoload_with=db.engine)
    # total_table = db.metadata.tables['v_time_order_count']
    data = db.session.query(total_table_static.c.count_num).all()
    result = []
    for i in data:
        result.append(i[0])

    # overtime alert realtime
    total_table = Table('v_no_time_count', db.metadata, autoload=True, autoload_with=db.engine)
    # total_table = db.metadata.tables['v_time_order_count']
    data = db.session.query(total_table.c.count_num).all()
    result1 = []
    for i in data:
        result1.append(i[0])
    total_realsum = sum(result1)

    # total order
    total_table2 = Table('v_no_time_sum', db.metadata, autoload=True, autoload_with=db.engine)
    data2 = db.session.query(total_table2.c.count_num).all()
    result2 = []
    for i in data2:
        result2.append(i[0])

    # pos = np.argwhere(np.array(result2)>0)[-1][0]
    # result2[:pos+1] = np.cumsum(result2[:pos+1])

    json = {'result':result, 'result2':result2, 'total_realsum':total_realsum}
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


app.register_blueprint(bp, url_prefix='/bigscreen')


def main():
    app.run(host='127.0.0.1', port='8000', debug=True)


if __name__ == '__main__':
    main()
