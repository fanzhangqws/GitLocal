from flask import jsonify, request
from flask_login import login_required, current_user
from api import app, db, login_manager
from api.common import make_return
from app.models import UserTable, BuildingTable, ClientTable
import datetime
import sqlalchemy
import numpy as np


# 获取楼宇列表
@app.route('/infocollect/showbuilding', methods=['POST'])
@login_required
def show_building():
    json = request.json

    pageNum = json.get('pageNum')
    pageSize = json.get('pageSize')
    data = []

    # get user id    
    user=current_user
    user_id = user.id

    building_table = db.session.query(BuildingTable).filter(
        BuildingTable.contractor_id==user_id)

    for raw_data in building_table:
        temp = {
            "id": raw_data.id,
            "building_name": raw_data.building_name
        }
        data.append(temp)

    data = sorted(data, key=lambda x: x["id"])

    totalPage = int(np.ceil(len(data)/pageSize))
    data = data[(pageNum-1)*pageSize:pageNum*pageSize]
    
    return make_return(success=True, message='获取楼宇列表成功', 
        data={'building': data,'totalPage':totalPage})


# 获取客户信息列表
@app.route('/infocollect/clientlist', methods=['POST'])
@login_required
def client_list():
    json = request.json
    query = json.get('query')
    building_id = json.get('building_id')
    pageNum = json.get('pageNum')
    pageSize = json.get('pageSize')
    data = []

    # get user id
    user=current_user

    client_table = db.session.query(ClientTable).filter(
        ClientTable.building_id==building_id)

    # filter by client name or no filter
    if query!='':
        client_list = client_table.filter(ClientTable.company_name.like('%'+query+'%'))
    else:
        client_list = client_table
    for raw_data in client_list:
        temp = {
            "id": raw_data.id,
            "company_name": raw_data.company_name
        }

        data.append(temp)
    data = sorted(data, key=lambda x: x["id"])
    print('len(data)',len(data))
    totalPage = int(np.ceil(len(data)/pageSize))
    data = data[(pageNum-1)*pageSize:pageNum*pageSize]

    return make_return(success=True, message='获取客户列表成功', 
        data={'client': data,'totalPage':totalPage})


# 获取客户详情
@app.route('/infocollect/clientdetail', methods=['POST'])
@login_required
def client_detail():
    json = request.json
    query_id = json.get('id')
    data = []

    # get user id    
    user=current_user
    user_name = user.user_name
    user_dept = user.user_dept
    client_detail_info = db.session.query(ClientTable).filter(
        ClientTable.id == query_id).one_or_none()

    list_columns = ['company_name','employees_nbr','customer_industry',
        'customer_main_business','customer_marketing_model','key_person','job_title',
        'telephone_nbr_bussiness','phone_nbr','client_type','client_manager','client_manager_contact_nbr',
        'crm_client_name','client_id','represent_nbr','payment_nbr','monthly_income',
        'broadband_quantity','broadband_nbr','telephone_quantity','telephone_nbr','tianyi_nbr',
        'smart_company','smart_company_quantity','optical_fiber_access',
        'private_line_access_number','have_ip','ip_quantity','have_web','server','question_list',
        'opportunities_description','promotion_situation','problems_support',
        'broadband_belonging','broadband_bandwidth','broadband_cost',
        'telephone_cost','smart_company_plan','have_DIC',
        'DIC_nbr','DIC_line_nbr','DIC_cost', 'enemy_DIC_info',]

    if client_detail_info is None:
        raise ValueError('根据ID %d 找不到该用户'%query_id)
    else:
        item_list = [getattr(client_detail_info, x) for x in list_columns]

    return make_return(success=True, message='获取客户详情成功!', data={'item_list': item_list})

# 更新客户详情
@app.route('/infocollect/updateclientdetail', methods=['POST'])
@login_required
def update_client_detail():
    json = request.json
    query_id = json.get('client_id')
    item_list = json.get('item_list')

    # reverse value type frm string to int
    int_index = [1,13,14,15,16,17,19,21,23,27]
    for i in int_index:
        if item_list[i]!='':
            item_list[i] = int(item_list[i])
        else:
            item_list[i] = 0

    data = []

    # get user id    
    user=current_user
    user_name = user.user_name
    user_dept = user.user_dept
    client_detail_info = db.session.query(ClientTable).filter(
        ClientTable.id == query_id).one_or_none()

    list_columns = ['company_name','employees_nbr','customer_industry',
        'customer_main_business','customer_marketing_model','key_person','job_title',
        'telephone_nbr_bussiness','phone_nbr','client_type','client_manager','client_manager_contact_nbr',
        'crm_client_name','client_id','represent_nbr','payment_nbr','monthly_income',
        'broadband_quantity','broadband_nbr','telephone_quantity','telephone_nbr','tianyi_nbr',
        'smart_company','smart_company_quantity','optical_fiber_access',
        'private_line_access_number','have_ip','ip_quantity','have_web','server','question_list',
        'opportunities_description','promotion_situation','problems_support',
        'broadband_belonging','broadband_bandwidth','broadband_cost',
        'telephone_cost','smart_company_plan','have_DIC',
        'DIC_nbr','DIC_line_nbr','DIC_cost', 'enemy_DIC_info',]

    if client_detail_info is None:
        raise ValueError('根据ID %d 找不到该用户'%query_id)
    else:
        for i, item in enumerate(list_columns):
            if i == 0:
                continue
            setattr(client_detail_info, item, item_list[i])

    db.session.merge(client_detail_info)
    db.session.commit()
    errmsg = '客户详情更新成功!'
    return make_return(success=True, message=errmsg, data={})

# 获取物业信息详情
@app.route('/infocollect/buildingdetail', methods=['POST'])
@login_required
def building_detail():
    json = request.json
    query_id = json.get('id')
    data = []

    # get user id    
    user=current_user
    user_name = user.user_name
    user_dept = user.user_dept
    building_detail_info = db.session.query(BuildingTable).filter(
        BuildingTable.id == query_id).one_or_none()

    list_columns = ['building_name','grid_id','building_dept_nbr',
        'building_floor_nbr','delivery_year','FTTH_access','bussiness_nbr',
        'average_rental','access_method','circus_belongings','hoistgate_belongings',
        'property_management_company','employees_nbr','estate_management_contact_person',
        'estate_management_contact_nbr','merchants_head','merchants_head_contact_nbr',
        'engineering_department_head','engineering_department_head_contact_nbr',
        'finance_department_head','finance_department_head_contact_nbr','branch',
        'located_contractor','marketing_service_manager','marketing_service_manager_contact_nbr',
        'maintenance_person','maintenance_person_contact_nbr']

    if building_detail_info is None:
        raise ValueError('根据ID %d 找不到该楼宇物业信息'%query_id)
    else:
        item_list = [getattr(building_detail_info, x) for x in list_columns]

    return make_return(success=True, message='获取客户详情成功!', data={'item_list': item_list})


# 更新物业信息详情
@app.route('/infocollect/updatebuildingdetail', methods=['POST'])
@login_required
def update_building_detail():
    json = request.json
    query_id = json.get('building_id')
    item_list = json.get('item_list')

    # reverse value type frm string to int
    int_index = [2,3,4,6,7,12]
    for i in int_index:
        if item_list[i]!='':
            item_list[i] = int(item_list[i])
        else:
            item_list[i] = 0

    data = []

    # get user id    
    user=current_user
    user_name = user.user_name
    user_dept = user.user_dept
    building_detail_info = db.session.query(BuildingTable).filter(
        BuildingTable.id == query_id).one_or_none()

    list_columns = ['building_name','grid_id','building_dept_nbr',
        'building_floor_nbr','delivery_year','FTTH_access','bussiness_nbr',
        'average_rental','access_method','circus_belongings','hoistgate_belongings',
        'property_management_company','employees_nbr','estate_management_contact_person',
        'estate_management_contact_nbr','merchants_head','merchants_head_contact_nbr',
        'engineering_department_head','engineering_department_head_contact_nbr',
        'finance_department_head','finance_department_head_contact_nbr','branch',
        'located_contractor','marketing_service_manager','marketing_service_manager_contact_nbr',
        'maintenance_person','maintenance_person_contact_nbr']

    if building_detail_info is None:
        raise ValueError('根据ID %d 找不到该用户'%query_id)
    else:
        for i, item in enumerate(list_columns):
            if i == 0:
                continue
            setattr(building_detail_info, item, item_list[i])

    db.session.merge(building_detail_info)
    db.session.commit()
    errmsg = '物业信息详情更新成功!'
    return make_return(success=True, message=errmsg, data={})


# 新增客户
@app.route('/infocollect/newclient', methods=['POST'])
@login_required
def new_client():
    json = request.json
    query_id = json.get('building_id')
    item_list = json.get('item_list')

    # reverse value type from string to int
    int_index = [1,13,14,15,16,17,19,21,23,27]
    for i in int_index:
        if item_list[i]!='':
            item_list[i] = int(item_list[i])
        else:
            item_list[i] = 0

    data = []

    # get user id    
    user=current_user
    user_name = user.user_name
    user_dept = user.user_dept
    client_detail_info = ClientTable()

    list_columns = ['company_name','employees_nbr','customer_industry',
        'customer_main_business','customer_marketing_model','key_person','job_title',
        'telephone_nbr_bussiness','phone_nbr','client_type','client_manager','client_manager_contact_nbr',
        'crm_client_name','client_id','represent_nbr','payment_nbr','monthly_income',
        'broadband_quantity','broadband_nbr','telephone_quantity','telephone_nbr','tianyi_nbr',
        'smart_company','smart_company_quantity','optical_fiber_access',
        'private_line_access_number','have_ip','ip_quantity','have_web','server','question_list',
        'opportunities_description','promotion_situation','problems_support']

    for i, item in enumerate(list_columns):
        setattr(client_detail_info, item, item_list[i])

    setattr(client_detail_info, 'building_id', query_id)

    db.session.merge(client_detail_info)
    db.session.commit()
    errmsg = '新增客户成功!'
    return make_return(success=True, message=errmsg, data={})









# 查看订单
@app.route('/order/detail', methods=['GET'])
@login_required
def order_detail():
    order_id = request.args.get('id')
    # get user id    
    user=current_user
    user_name = user.user_name
    user_dept = user.user_dept


    data = []
    # generate_info
    sla_mission_query = db.session.query(sla_mission).filter(sla_mission.ddid==order_id).first()
    order_table_name = sla_mission_query.ddb
    order_table = get_table_cls(order_table_name)
    order_data_query = db.session.query(order_table).filter(order_table.ddid==order_id).first()

    info_name = db.session.query(e2c).filter(e2c.table_name==order_table_name).order_by(e2c.x, e2c.y)
    info_list = []
    for query in info_name:
        info_list.append(
            {"label": query.cname, "value": getattr(order_data_query, query.ename.strip())}
            )
    
    # generate_log
    log_array = db.engine.execute('''
        select id, jdbm, case when overtime is null then '处理中' else '已处理' end, overtime, clnr from
        sla_mission, dis_sla_mission where sla_mission.ddid = dis_sla_mission.order_id
        and sla_mission.preorder_id = %s
        union all
        select id, jdbm, case when overtime is null then '处理中' else '已处理' end, overtime, clnr from
        sla_mission, dis_sla_mission2 where sla_mission.ddid = dis_sla_mission2.order_id
        and sla_mission.preorder_id = %s
        union all 
        select id, jdbm, case when overtime is null then '处理中' else '已处理' end, overtime, clnr from
        sla_mission, dis_sla_mission where sla_mission.ddid = dis_sla_mission.order_id
        and sla_mission.ddid = %s
        union all
        select id, jdbm, case when overtime is null then '处理中' else '已处理' end, overtime, clnr from
        sla_mission, dis_sla_mission2 where sla_mission.ddid = dis_sla_mission2.order_id
        and sla_mission.ddid = %s
        ''', (order_id, order_id, order_id, order_id)).fetchall()
    log_list=[]
    for item in log_array:
        temp = {"id": item[0], "workarea": item[1], "status": item[2], 
        "status_date": item[3], "content":item[4]}

        log_list.append(temp)

    # 待办工单id
    dis_sla_mission_id = db.session.query(dis_sla_mission.id).filter(
        dis_sla_mission.order_id==order_id, dis_sla_mission.jdbm.in_([user_name, user_dept]),
        dis_sla_mission.overtime==None).first()
    if dis_sla_mission_id is not None:
        data = {'attachment': [], 'logs': log_list, 'info': info_list, 'id': str(dis_sla_mission_id.id)}
    else:
        data = {'attachment': [], 'logs': log_list, 'info': info_list, 'id': ''}

    return make_return(success=True, message='获取订单详情成功!', data=data)


# 工单处理
@app.route('/order/process', methods=['POST'])
@login_required
def order_process():
    json = request.json
    return_id = int(json.get('id'))
    path = json.get('path')
    targets = json.get('targets')
    score = json.get('score')
    memo = json.get('memo')

    # get user id    
    user=current_user
    user_name = user.user_name
    user_dept = user.user_dept

    data = []
    try:
        # update dis_sla_mission
        dis_sla_mission_query = db.session.query(dis_sla_mission).filter(
            dis_sla_mission.id==return_id).first()
        dis_sla_mission_query.overtime = datetime.datetime.now()

        # add score record
        raw_data = dis_sla_score()
        raw_data.disid=return_id
        raw_data.score=score
        raw_data.created_by=user_name
        raw_data.created_on=datetime.datetime.now()
        db.session.add(raw_data)

        # update sla_mission
        ddid = dis_sla_mission_query.order_id
        sla_mission_query = db.session.query(sla_mission).filter(sla_mission.ddid==ddid).first()
        if len(targets) > 1:
            sla_mission_query.ddwz ='多部门'
        if len(targets) == 1:
            sla_mission_query.ddwz = targets[0]
            if targets[0].strip() == '工单竣工':
                sla_mission_query.ddzt = 1

        # insert dis_sla_mission 
        for target in targets:
            if target.strip() == '发单部门':
               target = sla_mission_query.fddw
            elif target.strip() == '上一环节':
               target = dis_sla_mission_query.fdbm
            elif target.strip() == '发单人':
               target = sla_mission_query.fdr

            if target.strip() == '工单竣工':
                continue    

            raw_data2 = dis_sla_mission()
            raw_data2.order_id = ddid
            raw_data2.order_type = 0
            raw_data2.jdbm=target
            raw_data2.czfs=path
            raw_data2.fdbm=user_dept
            raw_data2.main_dept = target
            raw_data2.clnr=memo
            raw_data2.clr=user_name
            setattr(raw_data2, 'class', getattr(sla_mission_query, 'class'))
            raw_data2.addtime=datetime.datetime.now()
            raw_data2.overtime=None

            db.session.add(raw_data2)
            app.logger.info('insert dis_sla_mission %s' % target)

        db.session.commit()
        return make_return(success=True, message='工单处理成功!', data={})
    except Exception as e:
        db.session.rollback()
        app.logger.exception(e)
        return make_return(success=False, message='工单处理失败!', data={})


# 撤单
@app.route('/order/cancel', methods=['POST'])
@login_required
def order_cancel_func():
    json = request.json
    order_id = json.get('id')
    reason = json.get('reason')

    # get user id    
    user=current_user
    user_name = user.user_name
    user_dept = user.user_dept


    # input variables verification
    if reason=="":
        return make_return(success=False, message='撤单原因不能为空！', data={})
    if order_id=="":
        return make_return(success=False, message='订单ID不能为空, 请重新打开本页面！', data={})

    # generate order id
    serial_number = get_serial_number("cd99")

    # find destination dept
    desti_dept = db.session.query(sla_kx_cllc.l_a_dept).filter(
        sla_kx_cllc.l_flow_name == '订单发送', sla_kx_cllc.l_type == '发送工单', 
        sla_kx_cllc.l_s_dept == user_dept, sla_kx_cllc.l_ywlx == '客户经理撤单').first()
    if desti_dept is None:
        app.logger.error('工单撤销无法找到目的部门！')
        return make_return(success=False, message='工单撤销无法找到目的部门！', data={})

    try:
        # insert order_cancel
        raw_data = order_cancel()
        raw_data.ddid = serial_number
        raw_data.cancel_ddid = order_id
        raw_data.reason = reason
        raw_data.created_by = user_name
        raw_data.created_on = datetime.datetime.now()
        db.session.add(raw_data)

        # insert sla_mission
        raw_data2 = sla_mission()
        raw_data2.ddid = serial_number
        raw_data2.ycdid = None
        raw_data2.ddlx = 79
        raw_data2.ddb ='order_cancel'
        raw_data2.fddw = user_dept
        raw_data2.dddj = '普通'
        raw_data2.fdrq = datetime.datetime.now()
        raw_data2.fdr = user_name
        raw_data2.ddwz = desti_dept
        raw_data2.ddzt = 0
        raw_data2.ywlx = '客户经理撤单'
        raw_data2.yhmc = None
        raw_data2.ktfwdj = None
        raw_data2.htqdrq = None
        raw_data2.ktlb = None
        raw_data2.xyzsr = 0
        raw_data2.wlcb = 0
        raw_data2.fxpcj = 0
        raw_data2.yhdz = None
        setattr(raw_data2, 'class', 3)
        db.session.add(raw_data2)

        # insert dis_sla_mission 
        raw_data3 = dis_sla_mission()
        raw_data3.order_id = serial_number
        raw_data3.order_type = 79
        raw_data3.fdbm = user_dept
        raw_data3.jdbm = desti_dept
        raw_data3.addtime = datetime.datetime.now()
        raw_data3.overtime = None
        raw_data3.czfs = '下订单'
        raw_data3.clnr = '下订单'
        raw_data3.clr = None
        setattr(raw_data3, 'class', 3)
        db.session.add(raw_data3)

        db.session.commit()
        return make_return(success=True, message='撤单成功!', data={})
    except Exception as e:
        db.session.rollback()
        app.logger.exception(e)
        return make_return(success=False, message='撤单失败!', data={})


# 获取工单处理类型
@app.route('/order/get_next', methods=['GET'])
@login_required
def order_get_next():
    order_id = request.args.get('id')
    if order_id[-1]=="0":
        aa = "预测"
    elif order_id[-1]=="1":
        aa = "资源调查"
    else:
        aa = "订单发送"
    # get user dept    
    user=current_user
    user_dept = user.user_dept

    # from order_id get corresponding order type
    sla_mission_query = db.session.query(sla_mission).filter(sla_mission.ddid==order_id).one_or_none()
    if sla_mission_query is None:
        app.logger.error('order id %s is not found in table sla_mission!' %(order_id) )
        return make_return(success=False, message='该工单不存在！', data={})

    order_type = sla_mission_query.ywlx

    # get action type
    sla_kx_cllc_query = db.session.query(sla_kx_cllc).filter(
        sla_kx_cllc.l_s_dept==user_dept, 
        sla_kx_cllc.l_ywlx==order_type, 
        sla_kx_cllc.l_flow_name==aa).all()

    data_output = []
    for query in sla_kx_cllc_query:
        path_item = query.l_type
        target_item = query.l_a_dept
        targets_output = []

        if target_item.strip()=="选择部门":
            target_list = query.l_xzbm.split(',')
            for j in target_list:
                targets_output.append({"name": j, "target_id": j})

        else:
            targets_output = [{"name": target_item, "target_id": target_item}]

        out_item = {"path": path_item, "targets": targets_output}
        data_output.append(out_item)
    if len(data_output)==0:
        return make_return(success=False, message='该岗位无处理流程!', data=data_output)
    else:
        return make_return(success=True, message='获取工单处理类型成功!', data=data_output)


# 工单发起
@app.route('/order/create', methods=['POST'])
@login_required
def order_create():
    json = request.json
    order_type = json.get('order_type')
    cust_name = json.get('cust_name')
    cust_id = json.get('cust_id')
    a_contact = json.get('a_contact')
    a_contact_phone = json.get('a_contact_phone')
    a_address = json.get('a_address')
    z_contact = json.get('z_contact')
    z_contact_phone = json.get('z_contact_phone')
    z_address = json.get('z_address')
    attachment = json.get('attachment')

    # get user id    
    user=current_user
    user_name = user.user_name
    user_dept = user.user_dept

    # generate order id
    serial_number = get_serial_number("sd99")

    # find destination dept
    desti_dept = db.session.query(sla_kx_cllc.l_a_dept).filter(
        sla_kx_cllc.l_flow_name == '订单发送', sla_kx_cllc.l_type == '发送工单', 
        sla_kx_cllc.l_s_dept == user_dept, sla_kx_cllc.l_ywlx == '客户经理甩单').first()
    if desti_dept is None:
        app.logger.error('工单发起无法找到目的部门！')
        return make_return(success=False, message='工单发起无法找到目的部门！', data={})

    try:
        # insert order_pre
        raw_data = order_pre()
        raw_data.ddid = serial_number
        raw_data.order_type = order_type
        raw_data.cust_name = cust_name
        raw_data.cust_id = cust_id
        raw_data.a_contact = a_contact
        raw_data.a_contact_phone = a_contact_phone
        raw_data.a_address = a_address
        raw_data.z_contact = z_contact
        raw_data.z_contact_phone = z_contact_phone
        raw_data.z_address = z_address

        raw_data.created_by = user_name
        raw_data.created_on = datetime.datetime.now()
        db.session.add(raw_data)

        # insert sla_mission
        raw_data2 = sla_mission()
        raw_data2.ddid = serial_number
        raw_data2.ycdid = None
        raw_data2.ddlx = 78
        raw_data2.ddb ='order_pre'
        raw_data2.fddw = user_dept
        raw_data2.dddj = '普通'
        raw_data2.fdrq = datetime.datetime.now()
        raw_data2.fdr = user_name
        raw_data2.ddwz = desti_dept
        raw_data2.ddzt = 0
        raw_data2.ywlx = '客户经理甩单'
        raw_data2.yhmc = cust_name
        raw_data2.ktfwdj = None
        raw_data2.htqdrq = None
        raw_data2.ktlb = None
        raw_data2.xyzsr = 0
        raw_data2.wlcb = 0
        raw_data2.fxpcj = 0
        raw_data2.yhdz = a_address
        setattr(raw_data2, 'class', 3)
        db.session.add(raw_data2)

        # insert dis_sla_mission 
        raw_data3 = dis_sla_mission()
        raw_data3.order_id = serial_number
        raw_data3.order_type = 79
        raw_data3.fdbm = user_dept
        raw_data3.jdbm = desti_dept
        raw_data3.addtime = datetime.datetime.now()
        raw_data3.overtime = None
        raw_data3.czfs = '下订单'
        raw_data3.clnr = '下订单'
        raw_data3.clr = user_name
        setattr(raw_data3, 'class', 3)
        db.session.add(raw_data3)
        db.session.flush()
        # update sla_gx_file
        for attachment_id in attachment:
            query = db.session.query(sla_gx_file).filter(sla_gx_file.ID==attachment_id).first()
            if query is not None:
                query.orderid = serial_number
                query.disid = raw_data3.id
            else:
                app.logger.error('工单发起无法找到附件！')

        db.session.commit()
        return make_return(success=True, message='工单发起成功!', data={})
    except Exception as e:
        db.session.rollback()
        app.logger.exception(e)
        return make_return(success=False, message='工单发起失败!', data={})
