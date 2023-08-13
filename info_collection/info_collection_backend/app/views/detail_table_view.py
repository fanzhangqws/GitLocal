from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, AppBuilder, expose, BaseView, has_access
from app import appbuilder, db
from app.models import BuildingTable, UserTable, ClientTable
from flask_appbuilder.models.sqla.filters import FilterNotEqual

class User_Table_View(ModelView):
    datamodel = SQLAInterface(UserTable)
    list_title = '用户信息表'
    label_columns = {'user_name': '用户姓名', 'user_dept': '所属部门/分公司', 
        'phone_nbr': '电话', 'password': '密码', 'contractor_group':'承包体',
        'is_authenticated':'授权'}
    list_columns = ['id','user_name','user_dept','contractor_group','phone_nbr',
        'password','is_authenticated']


class Building_Table_View(ModelView):
    datamodel = SQLAInterface(BuildingTable)
    list_title = '物业信息表'
    # base_filters = [['ordertype', FilterNotEqual, '6'], ['ordertype', FilterNotEqual, '7'], 
    # ['status',FilterNotEqual, 'C']]
    label_columns = {'contractor_id': '承包人id', 'building_name': '楼宇名称', 
        'grid_id': '网格编号', 'building_dept_nbr': '楼宇栋数', 'building_floor_nbr': '楼层数', 
        'delivery_year': '交付年限', 'FTTH_access': 'FTTH接入', 'bussiness_nbr': '商户数', 
        'average_rental': '平均租金（元/㎡）', 'access_method': '线路接入方式', 
        'circus_belongings': '线路产权', 'hoistgate_belongings': '井道的线槽归属', 
        'property_management_company': '物管公司', 'employees_nbr': '员工数', 
        'estate_management_contact_person': '物管决策联系人', 
        'estate_management_contact_nbr': '物管决策联系人联系方式', 
        'merchants_head': '招商部/中介/客服部负责人', 
        'merchants_head_contact_nbr': '招商部/中介/客服部负责人联系方式', 
        'engineering_department_head': '工程部负责人', 
        'engineering_department_head_contact_nbr': '工程部负责人联系方式', 
        'finance_department_head': '财务部负责人', 
        'finance_department_head_contact_nbr': '财务部负责人联系方式', 'branch': '所在分公司', 
        'located_contractor': '所在承包体/中心', 'marketing_service_manager': '营销服务经理', 
        'marketing_service_manager_contact_nbr': '营销服务联系方式', 
        'maintenance_person': '装维人员', 'maintenance_person_contact_nbr': '装维人员联系方式'}
    list_columns = ['id','contractor_id','building_name','grid_id','building_dept_nbr',
        'building_floor_nbr','delivery_year','FTTH_access','bussiness_nbr',
        'average_rental','access_method','circus_belongings','hoistgate_belongings',
        'property_management_company','employees_nbr','estate_management_contact_person',
        'estate_management_contact_nbr','merchants_head','merchants_head_contact_nbr',
        'engineering_department_head','engineering_department_head_contact_nbr',
        'finance_department_head','finance_department_head_contact_nbr','branch',
        'located_contractor','marketing_service_manager','marketing_service_manager_contact_nbr',
        'maintenance_person','maintenance_person_contact_nbr']

class Client_Table_View(ModelView):
    datamodel = SQLAInterface(ClientTable)
    list_title = '客户信息表'
    label_columns = {'building_id': '所属楼宇id', 'company_name': '公司名称', 
        'employees_nbr': '员工数量', 'customer_industry': '客户行业', 
        'customer_main_business': '客户主营业务', 'customer_marketing_model': '客户营销模式', 
        'key_person': '关键人', 'job_title': '职务', 'telephone_nbr_bussiness': '办公固话号', 
        'phone_nbr': '手机号码', 'client_type': '客户类型', 'client_manager': '营销服务客户经理', 
        'client_manager_contact_nbr': '营销服务客户经理联系方式', 
        'crm_client_name': 'CRM系统客户名称', 
        'client_id': '客户ID', 'represent_nbr': '代表号码', 'payment_nbr': '付费编码', 
        'monthly_income': '月收入', 'broadband_quantity': '宽带数量', 'broadband_nbr': '宽带号', 
        'telephone_quantity': '固话数量', 'telephone_nbr': '固话号', 'tianyi_nbr': '天翼数量', 
        'smart_company': '智慧企业', 
        'smart_company_quantity': '智慧企业数量', 'optical_fiber_access': '是否有光纤专线接入', 
        'private_line_access_number': '专线接入号', 'have_ip': '是否有IP', 
        'ip_quantity': 'IP数量', 'have_web': '是否有网站', 'server': '服务器', 
        'question_list': '问题清单', 'opportunities_description': '业务需求及商机描述', 
        'promotion_situation': '商机推进情况', 'problems_support': '存在的问题及支撑需求',
        'broadband_belonging':'宽带归属','broadband_bandwidth':'宽带带宽',
        'broadband_cost':'宽带费用或者套餐','telephone_cost':'固话月消费',
        'smart_company_plan':'智慧企业套餐','have_DIC':'是否有数字电路','DIC_nbr':'数字电路数量',
        'DIC_line_nbr':'数字电路条数', 'DIC_cost':'数字电路总费用',
        'enemy_DIC_info':'异网数字电路情况'}
    list_columns = ['id','building_id','company_name','employees_nbr','customer_industry',
        'customer_main_business','customer_marketing_model','key_person','job_title',
        'telephone_nbr_bussiness','phone_nbr','client_type','client_manager',
        'client_manager_contact_nbr',
        'crm_client_name','client_id','represent_nbr','payment_nbr','monthly_income',
        'broadband_quantity','broadband_nbr','broadband_belonging','broadband_bandwidth',
        'broadband_cost','telephone_quantity','telephone_nbr','telephone_cost','tianyi_nbr',
        'smart_company','smart_company_plan','smart_company_quantity','optical_fiber_access',
        'private_line_access_number','have_ip','ip_quantity','have_DIC','DIC_nbr','DIC_line_nbr',
        'DIC_cost','enemy_DIC_info','have_web','server','question_list',
        'opportunities_description','promotion_situation','problems_support']


db.create_all()


appbuilder.add_view(User_Table_View,
                    "用户信息表",
                    icon = "fa-user",
                    category = "全部数据")

appbuilder.add_view(Building_Table_View,
                    "物业信息表",
                    icon = "fa-home",
                    category = "全部数据")

appbuilder.add_view(Client_Table_View,
                    "客户信息表",
                    icon = "fa-phone",
                    category = "全部数据")