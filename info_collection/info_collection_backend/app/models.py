from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Integer
from sqlalchemy.orm import relationship


class UserTable(Model):
    # 用户信息表
    __tablename__ = 'UserTable'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(200)) #用户姓名
    user_dept = Column(String(200)) #所属部门/分公司
    contractor_group = Column(String(200)) #承包体
    phone_nbr = Column(Integer())   #电话
    password = Column(String(200))  #密码
    is_authenticated = Column(Integer()) 


class BuildingTable(Model):
    # 物业信息表
    __tablename__ = 'BuildingTable'
    id = Column(Integer, primary_key=True)
    contractor_id = Column(Integer(), ForeignKey('UserTable.id'), nullable=False)   #承包人id
    building_name = Column(String(200))                             #楼宇名称
    grid_id = Column(String(200))                                   #网格编号
    building_dept_nbr = Column(Integer())                           #楼宇栋数
    building_floor_nbr = Column(Integer())                          #楼层数
    delivery_year = Column(Integer())                               #交付年限
    FTTH_access = Column(String(200))                               #FTTH接入
    bussiness_nbr = Column(Integer())                               #商户数
    average_rental = Column(Integer())                                #平均租金（元/㎡）
    access_method = Column(String(200))                             #线路接入方式
    circus_belongings = Column(String(200))                         #线路产权
    hoistgate_belongings = Column(String(200))                      #井道的线槽归属
    property_management_company = Column(String(200))               #物管公司
    employees_nbr = Column(Integer())                               #员工数
    estate_management_contact_person = Column(String(200))          #物管决策联系人
    estate_management_contact_nbr = Column(String(200))               #物管决策联系人联系方式
    merchants_head = Column(String(200))                            #招商部/中介/客服部负责人
    merchants_head_contact_nbr = Column(String(200))                  #招商部/中介/客服部负责人联系方式
    engineering_department_head =  Column(String(200))              #工程部负责人
    engineering_department_head_contact_nbr = Column(String(200))     #工程部负责人联系方式
    finance_department_head =  Column(String(200))                  #财务部负责人
    finance_department_head_contact_nbr = Column(String(200))         #财务部负责人联系方式
    branch =  Column(String(200))                                   #所在分公司
    located_contractor =  Column(String(200))                       #所在承包体/中心
    marketing_service_manager = Column(String(200))                 #营销服务经理
    marketing_service_manager_contact_nbr = Column(String(200))       #营销服务联系方式
    maintenance_person = Column(String(200))                        #装维人员
    maintenance_person_contact_nbr = Column(String(200))              #装维人员联系方式


class ClientTable(Model):
    # 客户信息表
    __tablename__ = 'ClientTable'
    id = Column(Integer, primary_key=True)
    building_id = Column(Integer(), ForeignKey('BuildingTable.id'), nullable=False)     #所属楼宇id
    company_name = Column(String(200))                          #公司名称
    employees_nbr = Column(Integer())                           #员工数量
    customer_industry = Column(String(200))                     #客户行业
    customer_main_business = Column(String(200))                #客户主营业务
    customer_marketing_model = Column(String(200))              #客户营销模式
    key_person = Column(String(200))                            #关键人
    job_title = Column(String(200))                             #职务
    telephone_nbr_bussiness = Column(String(200))               #办公电话
    phone_nbr = Column(String(200))                             #手机号码
    client_type = Column(String(200))                           #客户类型
    client_manager = Column(String(200))                        #营销服务客户经理
    client_manager_contact_nbr = Column(String(200))            #营销服务客户经理联系方式
    crm_client_name = Column(String(200))                       #CRM系统客户名称
    client_id = Column(Integer())                               #客户ID
    represent_nbr = Column(Integer())                           #代表号码
    payment_nbr = Column(Integer())                             #付费编码
    monthly_income = Column(Integer())                          #月收入
    broadband_quantity = Column(Integer())                      #宽带数量
    broadband_nbr = Column(String(200))                         #宽带号
    broadband_belonging = Column(String(200))                         #宽带归属
    broadband_bandwidth = Column(String(200))                         #宽带带宽
    broadband_cost = Column(String(200))                              #宽带费用或者套餐
    telephone_quantity = Column(Integer())                      #固话数量
    telephone_nbr = Column(String(200))                         #固话号
    telephone_cost = Column(String(200))                              #固话月消费
    tianyi_nbr = Column(Integer())                              #天翼数量
    smart_company = Column(String(200))                         #智慧企业
    smart_company_plan = Column(String(200))                          #智慧企业套餐
    smart_company_quantity = Column(Integer())                  #智慧企业数量
    optical_fiber_access = Column(String(200))                  #是否有光纤专线接入
    private_line_access_number = Column(String(200))            #专线接入号
    have_ip = Column(String(200))                               #是否有IP
    ip_quantity = Column(Integer())                             #IP数量
    have_DIC = Column(Integer())                                      #是否有数字电路
    DIC_nbr = Column(Integer())                                       #数字电路数量
    DIC_line_nbr = Column(Integer())                                  #数字电路条数
    DIC_cost = Column(Integer())                                      #数字电路总费用
    enemy_DIC_info = Column(Integer())                                #异网数字电路情况
    have_web = Column(String(200))                              #是否有网站
    server = Column(String(200))                                #服务器
    question_list = Column(String(200))                         #问题清单
    opportunities_description = Column(String(200))             #业务需求及商机描述
    promotion_situation = Column(String(200))                   #商机推进情况
    problems_support = Column(String(200))                      #存在的问题及支撑需求
