from flask import Flask, request, render_template, jsonify, Blueprint, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Sequence
import flask
import os
import datetime
from sqlalchemy import Table
from flask import Flask, current_app, request, session,Response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_principal import Principal, Identity, AnonymousIdentity, identity_changed
import pandas as pd
from io import BytesIO

download_plan_table=[]
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://xxxx:xxxx@(DESCRIPTION=\
        (ADDRESS=(PROTOCOL=TCP)(HOST=x.x.x.x)(PORT=xxxx))(CONNECT_DATA=(SERVICE_NAME=develop)))'
app.config['APPLICATION_ROOT'] = '/balance'
db = SQLAlchemy(app)
db.metadata.reflect(bind=db.engine, views=True)

bp = Blueprint('balance', __name__, template_folder='templates',
               static_folder='static')

@bp.route('/',methods=['GET'])
def show_page():
    return render_template('upload.html')

@bp.route('/input_data', methods=['POST'])
def input_data():
    errcode = 0
    errmsg = ''
    file_name = request.files['importfile']
    df_blank = pd.read_excel(file_name)
    df = df_blank.dropna(how='all')
    df = df.where(pd.notnull(df), '0')
    seq = Sequence('fancy_num')
    balance_plan_detail_table = db.metadata.tables['balance_plan_detail_table']
    balance_monthly_data_table = db.metadata.tables['balance_monthly_data_table']
    balance_plan_table = db.metadata.tables['balance_plan_table']
    try:
        for i in df.index:
            row_content = df.loc[i]
            # check detail table existence
            if_detail_exist = db.session.query(balance_plan_detail_table).filter(
                balance_plan_detail_table.c.first_class == row_content[0],
                balance_plan_detail_table.c.second_class == row_content[1],
                balance_plan_detail_table.c.third_class == row_content[2],
                balance_plan_detail_table.c.cost_type == row_content[3],
                balance_plan_detail_table.c.region_type == row_content[4],
                balance_plan_detail_table.c.channel_type == row_content[5]).one_or_none()
            
            if if_detail_exist:
                row_id = if_detail_exist.row_id
            else:
                # 新增报表
                row_id = db.session.execute(seq)
                stmt = balance_plan_detail_table.insert().\
                    values(row_id=row_id,
                           first_class = row_content[0],
                           second_class = row_content[1],
                           third_class = row_content[2],
                           cost_type = row_content[3],
                           region_type = row_content[4],
                           channel_type = row_content[5])
                db.session.execute(stmt)
                db.session.commit()

            #------------------------------------------------------------------#
            # check plan table existence
            if_table_exist = db.session.query(balance_plan_table).filter(
                balance_plan_table.c.plan_input_id == row_content[8],
                balance_plan_table.c.plan_name == row_content[9],
                balance_plan_table.c.plan_generate_name == row_content[12]).one_or_none()
            # print("if_table_exist: ",if_table_exist)
            if if_table_exist:
                # print('haha,exist!')
                plan_id = if_table_exist.plan_id
                stmt = balance_plan_table.update().\
                where(balance_plan_table.c.plan_id == plan_id).\
                values(plan_value = float(row_content[10]),
                       credit_value = float(row_content[11]),
                       plan_generate_name = row_content[12],
                       plan_type = row_content[6],
                       mobile_side_type = row_content[7])
                db.session.execute(stmt)
                db.session.commit()
            else:
                # 新增报表
                plan_id = db.session.execute(seq)
                stmt = balance_plan_table.insert().\
                    values(plan_id=plan_id,
                           plan_input_id=row_content[8],
                           plan_name = row_content[9],
                           plan_value = float(row_content[10]),
                           credit_value = float(row_content[11]),
                           plan_generate_name = row_content[12],
                           plan_type = row_content[6],
                           mobile_side_type = row_content[7])
                db.session.execute(stmt)
                db.session.commit()
            print('pass!')
            #------------------------------------------------------------------#
            # check data table existence
            if_data_exist = db.session.query(balance_monthly_data_table).filter(
                balance_monthly_data_table.c.plan_id == plan_id,
                balance_monthly_data_table.c.row_id == row_id).one_or_none()
            
            if row_content[26]=='0':
                row_content[26]='无'
            print(row_content[26])
            if if_data_exist:
                # update data table
                data_id = if_data_exist.id
                stmt = balance_monthly_data_table.update().where(
                    balance_monthly_data_table.c.id == data_id).values(
                    t0=float(row_content[13]),
                    t1=float(row_content[14]),
                    t2=float(row_content[15]),
                    t3=float(row_content[16]),
                    t4=float(row_content[17]),
                    t5=float(row_content[18]),
                    t6=float(row_content[19]),
                    t7=float(row_content[20]),
                    t8=float(row_content[21]),
                    t9=float(row_content[22]),
                    t10=float(row_content[23]),
                    t11=float(row_content[24]),
                    t12=float(row_content[25]),
                    note=row_content[26])
                db.session.execute(stmt)
                db.session.commit()
            else:
                # 新增报表
                data_id = db.session.execute(seq)
                stmt = balance_monthly_data_table.insert().\
                values(plan_id=plan_id,
                    id = data_id,
                    row_id=row_id,
                    t0=float(row_content[13]),
                    t1=float(row_content[14]),
                    t2=float(row_content[15]),
                    t3=float(row_content[16]),
                    t4=float(row_content[17]),
                    t5=float(row_content[18]),
                    t6=float(row_content[19]),
                    t7=float(row_content[20]),
                    t8=float(row_content[21]),
                    t9=float(row_content[22]),
                    t10=float(row_content[23]),
                    t11=float(row_content[24]),
                    t12=float(row_content[25]),
                    note=row_content[26])

                db.session.execute(stmt)
                db.session.commit()
        errmsg = '上传成功!'
    except Exception as e:
        import traceback
        traceback.print_stack()
        errcode = -1
        errmsg = repr(e)

    return jsonify({"errcode": errcode, "errmsg": errmsg})


@bp.route('/list_data', methods=['GET'])
def list_data():
    balance_plan_table = db.metadata.tables['balance_plan_table']
    balance_plan_query= db.session.query(balance_plan_table)

    name_list = []; mobile_type_list = []; plan_type_list = []
    for x in balance_plan_query:
        if x.plan_generate_name and x.plan_generate_name not in name_list:
            name_list.append(x.plan_generate_name)
        if x.mobile_side_type and x.mobile_side_type not in mobile_type_list:
            mobile_type_list.append(x.mobile_side_type)
        if x.plan_type and x.plan_type not in plan_type_list:
            plan_type_list.append(x.plan_type)
   
    plan = {
            "plan_generate_name": name_list,
            "mobile_side_type": mobile_type_list,
            "plan_type": plan_type_list
        }

    balance_plan_detail_table = db.metadata.tables['balance_plan_detail_table']
    balance_plan_detail_query= db.session.query(balance_plan_detail_table)
    region_list=[]; channel_list=[]
    for x in balance_plan_detail_query:
        if x.region_type and x.region_type not in region_list and x.region_type!='全市':
            region_list.append(x.region_type)
        if x.channel_type and x.channel_type not in channel_list and x.channel_type!='全渠道':
            channel_list.append(x.channel_type)
    plan_detail = {
            "region_type": region_list,
            "channel_type": channel_list
        }

    json = {'plan': plan, 'plan_detail':plan_detail}     
    return jsonify(json)


@bp.route('/list_plan_data', methods=['GET'])
def list_plan_data():
    full_plan_info_table = db.metadata.tables['full_plan_info_table']
    full_plan_info_query= db.session.query(full_plan_info_table)
    plan_name=[]; plan_id=[]
    for x in full_plan_info_query:
        if x.销售品名称 and x.销售品名称 not in plan_name:
            plan_name.append(x.销售品名称)
        if x.销售品ID and x.销售品ID not in plan_id:
            plan_id.append(x.销售品ID)
    plan_serach_detail = {
            "plan_name":plan_name,
            "plan_id":plan_id
    }
    json = {'plan_serach_detail':plan_serach_detail}     
    return jsonify(json)

@bp.route('/search_coase',methods=['GET','POST'])
def search_coase_data():
    errcode = 0
    errmsg = ''
    
    if flask.request.method=='POST':        
        try:
            search_condition = request.json
            print(search_condition)

            balance_plan_detail_table = db.metadata.tables['balance_plan_detail_table']
            balance_monthly_data_table = db.metadata.tables['balance_monthly_data_table']
            balance_plan_table = db.metadata.tables['balance_plan_table']
            # find plan_id
            # print(search_condition["mobile_side_type"])
            if search_condition["mobile_side_type"]==[] and search_condition["plan_generate_name"]!=[] \
                                and search_condition["plan_type"]!=[]:
                plan_querys = db.session.query(balance_plan_table).filter(
                    balance_plan_table.c.plan_generate_name.in_(search_condition["plan_generate_name"]),
                    balance_plan_table.c.plan_type.in_(search_condition["plan_type"]))

            elif search_condition["mobile_side_type"]!=[] and search_condition["plan_generate_name"]!=[] \
                                and search_condition["plan_type"]!=[]:
                plan_querys = db.session.query(balance_plan_table).filter(
                    balance_plan_table.c.plan_generate_name.in_(search_condition["plan_generate_name"]),
                    balance_plan_table.c.plan_type.in_(search_condition["plan_type"]),
                    balance_plan_table.c.mobile_side_type.in_(search_condition["mobile_side_type"]))

            elif search_condition["mobile_side_type"]==[] and search_condition["plan_generate_name"]==[] \
                                and search_condition["plan_type"]!=[]:
                plan_querys = db.session.query(balance_plan_table).filter(
                    balance_plan_table.c.plan_type.in_(search_condition["plan_type"]))

            elif search_condition["mobile_side_type"]==[] and search_condition["plan_generate_name"]!=[] \
                                and search_condition["plan_type"]==[]:
                plan_querys = db.session.query(balance_plan_table).filter(
                    balance_plan_table.c.plan_generate_name.in_(search_condition["plan_generate_name"]))

            elif search_condition["mobile_side_type"]==[] and search_condition["plan_generate_name"]==[] \
                                and search_condition["plan_type"]==[]:
                plan_querys = db.session.query(balance_plan_table)

            elif search_condition["mobile_side_type"]!=[] and search_condition["plan_generate_name"]==[] \
                                and search_condition["plan_type"]==[]:
                plan_querys = db.session.query(balance_plan_table).filter(
                    balance_plan_table.c.mobile_side_type.in_(search_condition["mobile_side_type"]))

            elif search_condition["mobile_side_type"]!=[] and search_condition["plan_generate_name"]==[] \
                                and search_condition["plan_type"]!=[]:
                plan_querys = db.session.query(balance_plan_table).filter(
                    balance_plan_table.c.plan_type.in_(search_condition["plan_type"]),
                    balance_plan_table.c.mobile_side_type.in_(search_condition["mobile_side_type"]))

            elif search_condition["mobile_side_type"]!=[] and search_condition["plan_generate_name"]!=[] \
                                and search_condition["plan_type"]==[]:
                plan_querys = db.session.query(balance_plan_table).filter(
                    balance_plan_table.c.plan_generate_name.in_(search_condition["plan_generate_name"]),
                    balance_plan_table.c.mobile_side_type.in_(search_condition["mobile_side_type"]))

            plan_list = [[x.plan_id, x.mobile_side_type, x.plan_generate_name, \
                            x.plan_type] for x in plan_querys]
            print("finish plan search", plan_list)
            # find plan_detail_id
            if search_condition["region_type"]==[] and search_condition["channel_type"]!=[]:
                plan_detail_querys = db.session.query(balance_plan_detail_table).filter(
                    balance_plan_detail_table.c.channel_type.in_(search_condition["channel_type"]),
                    balance_plan_detail_table.c.region_type != '全市')
            elif search_condition["channel_type"]==[] and search_condition["region_type"]!=[]:
                plan_detail_querys = db.session.query(balance_plan_detail_table).filter(
                    balance_plan_detail_table.c.region_type.in_(search_condition["region_type"]),
                    balance_plan_detail_table.c.channel_type != '全渠道')
            elif search_condition["channel_type"]==[] and search_condition["region_type"]==[]:
                plan_detail_querys = db.session.query(balance_plan_detail_table).filter(
                    balance_plan_detail_table.c.region_type != '全市',
                    balance_plan_detail_table.c.channel_type != '全渠道')
            elif search_condition["channel_type"]!=[] and search_condition["region_type"]!=[]:
                plan_detail_querys = db.session.query(balance_plan_detail_table).filter(
                    balance_plan_detail_table.c.channel_type.in_(search_condition["channel_type"]),
                    balance_plan_detail_table.c.region_type.in_(search_condition["region_type"]))
            plan_detail_list = [[x.row_id, x.region_type, x.channel_type] for x in plan_detail_querys]
            print("finish plan_detail search",plan_detail_list)
            # find data table id and extract data
            result = []
            for plan_detail_item in plan_detail_list:
                for plan_item in plan_list:
                    if_data_exist = db.session.query(balance_monthly_data_table).filter(
                        balance_monthly_data_table.c.plan_id == plan_item[0],
                        balance_monthly_data_table.c.row_id == plan_detail_item[0]).one_or_none()
                    if if_data_exist:
                        feed_data = {
                            "region_type": plan_detail_item[1],
                            "channel_type": plan_detail_item[2],
                            "plan_type": plan_item[3],
                            "mobile_side_type": plan_item[1],
                            "plan_generate_name": plan_item[2],
                            }
                        if feed_data not in result:
                            result.append(feed_data)
            global result_table
            result_table = result
            print(result_table)
        except Exception as e:
            import traceback
            traceback.print_stack()
            errcode = -1
            errmsg = repr(e)

        return jsonify({"errcode": errcode, "errmsg": errmsg})
    else:
        return jsonify({"result": result_table})

@bp.route('/search',methods=['GET','POST'])
def search_data():
    errcode = 0
    errmsg = ''
    
    if flask.request.method=='POST':        
        try:
            search_condition = request.json
            print(search_condition)

            balance_plan_detail_table = db.metadata.tables['balance_plan_detail_table']
            balance_monthly_data_table = db.metadata.tables['balance_monthly_data_table']
            balance_plan_table = db.metadata.tables['balance_plan_table']
            # find plan_id
            print(search_condition["mobile_side_type"])
            if search_condition["plan_type"]!='全套餐':
                type_list = [search_condition["plan_type"],'全套餐']
            else:
                type_list = [search_condition["plan_type"]]
            plan_querys = db.session.query(balance_plan_table).filter(
                balance_plan_table.c.plan_generate_name == search_condition["plan_generate_name"],
                balance_plan_table.c.plan_type.in_(type_list),
                balance_plan_table.c.mobile_side_type == search_condition["mobile_side_type"])

            plan_list = [[x.plan_id, x.plan_value, x.credit_value, x.plan_generate_name]\
                                 for x in plan_querys]


            print("finish plan search")
            # find plan_detail_id
            if search_condition["channel_type"]!='全渠道':
                channel_list = [search_condition["channel_type"],'全渠道']
            else:
                channel_list = [search_condition["channel_type"]]

            if search_condition["region_type"]!='全市':
                region_list = [search_condition["region_type"],'全市']
            else:
                region_list = [search_condition["region_type"]]
            plan_detail_querys = db.session.query(balance_plan_detail_table).filter(
                balance_plan_detail_table.c.channel_type.in_(channel_list),
                balance_plan_detail_table.c.region_type.in_(region_list))
            plan_detail_list = [[x.row_id, x.first_class, x.second_class, x.third_class, x.cost_type] \
                                for x in plan_detail_querys]
            print("finish plan_detail search")
            # find data table id and extract data
            result = []
            for plan_detail_item in plan_detail_list:
                for plan_item in plan_list:
                    if_data_exist = db.session.query(balance_monthly_data_table).filter(
                        balance_monthly_data_table.c.plan_id == plan_item[0],
                        balance_monthly_data_table.c.row_id == plan_detail_item[0]).one_or_none()
                    if if_data_exist:
                        result.append({
                            "t2": plan_detail_item[1],
                            "t3": plan_detail_item[2],
                            "t4": plan_detail_item[3],
                            "t5": plan_detail_item[4],
                            "d1": plan_item[1],
                            "d2": plan_item[2],
                            "t1": plan_item[3],
                            "d3": if_data_exist.t0,
                            "d4": if_data_exist.t1,
                            "d5": if_data_exist.t2,
                            "d6": if_data_exist.t3,
                            "d7": if_data_exist.t4,
                            "d8": if_data_exist.t5,
                            "d9": if_data_exist.t6,
                            "d10": if_data_exist.t7,
                            "d11": if_data_exist.t8,
                            "d12": if_data_exist.t9,
                            "d13": if_data_exist.t10,
                            "d14": if_data_exist.t11,
                            "d15": if_data_exist.t12,
                            "d16": if_data_exist.total,
                            "d17": if_data_exist.note,
                            })
            global result_table
            result_table = result
        except Exception as e:
            import traceback
            traceback.print_stack()
            errcode = -1
            errmsg = repr(e)

        return jsonify({"errcode": errcode, "errmsg": errmsg})
    else:
        return jsonify({"result": result_table})

@bp.route('/search_plan',methods=['GET','POST'])
def search_plan():
    errcode = 0
    errmsg = ''
    
    if flask.request.method=='POST':        
        try:
            search_condition = request.json
            print(search_condition)

            full_plan_info_table = db.metadata.tables['full_plan_info_table']
            
            # find matched plan
            if search_condition["plan_name"] and search_condition["plan_id"]:
                plan_querys = db.session.query(full_plan_info_table).filter(
                    full_plan_info_table.c.销售品名称.like('%'+search_condition["plan_name"]+'%'),
                    full_plan_info_table.c.销售品ID == search_condition["plan_id"]).all()
            elif search_condition["plan_name"] and not search_condition["plan_id"]:
                plan_querys = db.session.query(full_plan_info_table).filter(
                    full_plan_info_table.c.销售品名称.like('%'+search_condition["plan_name"]+'%')).all()
            elif not search_condition["plan_name"] and search_condition["plan_id"]:
                plan_querys = db.session.query(full_plan_info_table).filter(
                    full_plan_info_table.c.销售品ID == search_condition["plan_id"]).all()
            else:
                plan_querys = db.session.query(full_plan_info_table)
            # find data table and extract data
            plan_serach_detail = [{
                    "plan_id": x.销售品ID,
                    "plan_name":x.销售品名称,
                    "plan_area":x.区域,
                    "eff_date":datetime.datetime.strftime(x.生效时间, '%Y-%m-%d') if x.生效时间 else '',
                    "exp_date":datetime.datetime.strftime(x.失效时间, '%Y-%m-%d') if x.失效时间 else '',
                    "status_cd":x.状态,
                    "protocol_life_cycle":x.协议期,
                    "offer_type":x.类型
            } for x in plan_querys]
            global result_table
            result_table = plan_serach_detail

            download_plan = [{
                    "销售品ID": x.销售品ID,
                    "销售品名称":x.销售品名称,
                    "区域":x.区域,
                    "生效时间":datetime.datetime.strftime(x.生效时间, '%Y-%m-%d') if x.生效时间 else '',
                    "失效时间":datetime.datetime.strftime(x.失效时间, '%Y-%m-%d') if x.失效时间 else '',
                    "状态":x.状态,
                    "协议期":x.协议期,
                    "类型":x.类型
            } for x in plan_querys]
            global download_plan_table
            download_plan_table = download_plan

        except Exception as e:
            import traceback
            traceback.print_stack()
            errcode = -1
            errmsg = repr(e)

        return jsonify({"errcode": errcode, "errmsg": errmsg})
    else:
        return jsonify({"result": result_table})

@bp.route('/download',methods=['GET'])
def download():
    print(download_plan_table)
    df = pd.DataFrame(download_plan_table)
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    output.seek(0)
    return send_file(output, attachment_filename='output.xlsx', as_attachment=True)

@bp.route('/save_table',methods=['POST'])
def save_table():
    form = request.json
    # print(table_data)
    errcode = 0
    errmsg = ''
    seq = Sequence('fancy_num')
    balance_plan_detail_table = db.metadata.tables['balance_plan_detail_table']
    balance_monthly_data_table = db.metadata.tables['balance_monthly_data_table']
    balance_plan_table = db.metadata.tables['balance_plan_table']

    #------------------------------------------------------------------#
    # check plan table existence
    if_table_exist = db.session.query(balance_plan_table).filter(
        balance_plan_table.c.mobile_side_type == form['mobile_side_type'],
        balance_plan_table.c.plan_type == form['plan_type'],
        balance_plan_table.c.plan_generate_name == form['plan_generate_name']).one_or_none()
    if if_table_exist:
        # print('haha,exist!')
        plan_id = if_table_exist.plan_id
    else:
        raise ValueError('plan_id does not exist!')

    # erase all data for balance data table with selected plan_id
    stmt = balance_monthly_data_table.delete().where(
            balance_monthly_data_table.c.plan_id == plan_id)
    db.session.execute(stmt)

    try:
        for row_content in form["table_data"]:
            # check detail table existence
            if_detail_exist = db.session.query(balance_plan_detail_table).filter(
                balance_plan_detail_table.c.first_class == row_content['t2'],
                balance_plan_detail_table.c.second_class == row_content['t3'],
                balance_plan_detail_table.c.third_class == row_content['t4'],
                balance_plan_detail_table.c.cost_type == row_content['t5'],
                balance_plan_detail_table.c.region_type == form['region_type'],
                balance_plan_detail_table.c.channel_type == form['channel_type']).one_or_none()
            
            if if_detail_exist:
                row_id = if_detail_exist.row_id
            else:
                # 新增报表
                row_id = db.session.execute(seq)
                stmt = balance_plan_detail_table.insert().\
                    values(row_id=row_id,
                           first_class = row_content['t2'],
                           second_class = row_content['t3'],
                           third_class = row_content['t4'],
                           cost_type = row_content['t5'],
                           region_type = form['region_type'],
                           channel_type = form['channel_type'])
                db.session.execute(stmt)
                db.session.commit()
            #------------------------------------------------------------------#
            # 新增报表
            data_id = db.session.execute(seq)
            stmt = balance_monthly_data_table.insert().\
            values(plan_id=plan_id,
                id = data_id,
                row_id=row_id,
                t0=float(row_content['d3']),
                t1=float(row_content['d4']),
                t2=float(row_content['d5']),
                t3=float(row_content['d6']),
                t4=float(row_content['d7']),
                t5=float(row_content['d8']),
                t6=float(row_content['d9']),
                t7=float(row_content['d10']),
                t8=float(row_content['d11']),
                t9=float(row_content['d12']),
                t10=float(row_content['d13']),
                t11=float(row_content['d14']),
                t12=float(row_content['d15']),
                total=float(row_content['d16']))
            db.session.execute(stmt)
            db.session.commit()
        errmsg = '上传成功!'
    except Exception as e:
        import traceback
        traceback.print_stack()
        errcode = -1
        errmsg = repr(e)

    return jsonify({"errcode": errcode, "errmsg": errmsg})
#---------------------------------------------------------------------#

app.register_blueprint(bp, url_prefix='/balance')

def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
