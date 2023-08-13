from flask import render_template, Flask, current_app, request, session 
from flask import Response, g, jsonify, send_file
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, AppBuilder, expose, BaseView, has_access
from app import appbuilder, db
import numpy
from app.models import UserTable, BuildingTable, ClientTable
import pandas as pd

class UploadUserExcel(BaseView):

    default_view = 'index'
    @expose('/upload')
    def index(self):
        return self.render_template('upload.html')

    @expose('/input_data', methods=['POST'])
    def input_data(self):
        errcode = 0
        errmsg = ''
        file_name = request.files['importfile']
        df = pd.read_excel(file_name)
        df.dropna(how='all',inplace=True)
        try:
            for i in df.index:
                row_content = df.loc[i]
                # check detail table existence
                raw_data = db.session.query(UserTable).filter(
                    UserTable.user_name == row_content[0],
                    UserTable.user_dept == row_content[1],
                    UserTable.phone_nbr == int(row_content[3])).one_or_none()
                
                if raw_data is None:
                    raw_data = UserTable()

                raw_data.user_name = row_content[0]
                raw_data.user_dept = row_content[1]
                raw_data.contractor_group = row_content[2]
                raw_data.phone_nbr = int(row_content[3])
                raw_data.password = (row_content[4] 
                    if row_content[4]!=None else 'E10ADC3949BA59ABBE56E057F20F883E')
                raw_data.is_authenticated = 1

                db.session.merge(raw_data)
                                
            db.session.commit()
            errmsg = '上传成功!'
        except Exception as e:
            import traceback
            traceback.print_stack()
            errcode = -1
            errmsg = repr(e)
            db.session.rollback()
            raise e

        return jsonify({"errcode": errcode, "errmsg": errmsg})

class UploadBuildingExcel(BaseView):

    default_view = 'index'
    @expose('/upload')
    def index(self):
        return self.render_template('upload.html')

    @expose('/input_data', methods=['POST'])
    def input_data(self):
        errcode = 0
        errmsg = ''
        file_name = request.files['importfile']
        df = pd.read_excel(file_name)
        df.dropna(how='all',inplace=True)
        try:
            for i in df.index:
                row_content = df.loc[i]
                print(row_content[0])

                # check contractor existence
                contractor_exist = db.session.query(UserTable).filter(
                    UserTable.user_name == row_content[0]).one_or_none()
                if contractor_exist is None:
                    raise ValueError('楼宇"%s"对应承包人不存在！'%(row_content[1]))

                # check BuildingTable existence
                raw_data = db.session.query(BuildingTable).filter(
                    BuildingTable.building_name == row_content[1]).one_or_none()
                
                if raw_data is None:
                    raw_data = BuildingTable()

                raw_data.contractor_id = contractor_exist.id
                raw_data.building_name = row_content[1]
                raw_data.grid_id = str(row_content[2])
                raw_data.building_dept_nbr = int(row_content[3])
                raw_data.building_floor_nbr = int(row_content[4])
                raw_data.delivery_year = int(row_content[5])
                raw_data.FTTH_access = row_content[6]
                raw_data.bussiness_nbr = int(row_content[7])
                raw_data.average_rental = int(row_content[8])
                raw_data.access_method = row_content[9]
                raw_data.circus_belongings = row_content[10]
                raw_data.hoistgate_belongings = row_content[11]
                raw_data.property_management_company = row_content[12]
                raw_data.employees_nbr = str(row_content[13])
                raw_data.estate_management_contact_person = row_content[14]
                raw_data.estate_management_contact_nbr = str(row_content[15])
                raw_data.merchants_head = row_content[16]
                raw_data.merchants_head_contact_nbr = str(row_content[17])
                raw_data.engineering_department_head = row_content[18]
                raw_data.engineering_department_head_contact_nbr = str(row_content[19])
                raw_data.finance_department_head = row_content[20]
                raw_data.finance_department_head_contact_nbr = str(row_content[21])
                raw_data.branch = row_content[22]
                raw_data.located_contractor = row_content[23]
                raw_data.marketing_service_manager = row_content[24]
                raw_data.marketing_service_manager_contact_nbr = str(row_content[25])
                raw_data.maintenance_person = row_content[26]
                raw_data.maintenance_person_contact_nbr = str(row_content[27])


                db.session.merge(raw_data)
                                
            db.session.commit()
            errmsg = '上传成功!'
        except Exception as e:
            import traceback
            traceback.print_stack()
            errcode = -1
            errmsg = repr(e)
            db.session.rollback()
            raise e

        return jsonify({"errcode": errcode, "errmsg": errmsg})

class UploadClientExcel(BaseView):

    default_view = 'index'
    @expose('/upload')
    def index(self):
        return self.render_template('upload.html')

    @expose('/input_data', methods=['POST'])
    def input_data(self):
        errcode = 0
        errmsg = ''
        file_name = request.files['importfile']
        df = pd.read_excel(file_name)
        df.dropna(how='all',inplace=True)
        try:
            for i in df.index:
                row_content = df.loc[i]

                # check Building existence
                building_exist = db.session.query(BuildingTable).filter(
                    BuildingTable.building_name == row_content[0]).one_or_none()
                if building_exist is None:
                    raise ValueError('客户"%s"对应楼宇不存在！'%(row_content[1]))

                # check Client existence
                raw_data = db.session.query(ClientTable).filter(
                    ClientTable.company_name == row_content[1]).one_or_none()
                
                if raw_data is None:
                    raw_data = ClientTable()
                raw_data.building_id = building_exist.id
                raw_data.company_name = row_content[1]
                raw_data.employees_nbr = int(row_content[2])
                raw_data.customer_industry = row_content[3]
                raw_data.customer_main_business = row_content[4]
                raw_data.customer_marketing_model = row_content[5]
                raw_data.key_person = row_content[6]
                raw_data.job_title = row_content[7]
                raw_data.telephone_nbr_bussiness = str(row_content[8])
                raw_data.phone_nbr = str(row_content[9])
                raw_data.client_type = row_content[10]
                raw_data.client_manager = row_content[11]
                raw_data.client_manager_contact_nbr = str(row_content[12])
                raw_data.crm_client_name = row_content[13]
                raw_data.client_id = int(row_content[14])
                raw_data.represent_nbr = int(row_content[15])
                raw_data.payment_nbr = int(row_content[16])
                raw_data.monthly_income = int(row_content[17])
                raw_data.broadband_quantity = int(row_content[18])
                raw_data.broadband_nbr = str(row_content[19])
                raw_data.telephone_quantity = int(row_content[20])
                raw_data.telephone_nbr = str(row_content[21])
                raw_data.tianyi_nbr = int(row_content[22])
                raw_data.smart_company = row_content[23]
                raw_data.smart_company_quantity = int(row_content[24])
                raw_data.optical_fiber_access = row_content[25]
                raw_data.private_line_access_number = row_content[26]
                raw_data.have_ip = row_content[27]
                raw_data.ip_quantity = int(row_content[28])
                raw_data.have_web = row_content[29]
                raw_data.server = row_content[30]
                raw_data.question_list = row_content[31]
                raw_data.opportunities_description = row_content[32]
                raw_data.promotion_situation = row_content[33]
                raw_data.problems_support = row_content[34]

                raw_data.broadband_belonging = row_content[35]
                raw_data.broadband_bandwidth = row_content[36]
                raw_data.broadband_cost = row_content[37]
                raw_data.telephone_cost = row_content[38]
                raw_data.smart_company_plan = row_content[39]
                raw_data.have_DIC = row_content[40]
                raw_data.DIC_nbr = row_content[41]
                raw_data.DIC_line_nbr = row_content[42]
                raw_data.DIC_cost = row_content[43]
                raw_data.enemy_DIC_info = row_content[44]

                db.session.merge(raw_data)
                                
            db.session.commit()
            errmsg = '上传成功!'
        except Exception as e:
            import traceback
            traceback.print_stack()
            errcode = -1
            errmsg = repr(e)
            db.session.rollback()
            raise e

        return jsonify({"errcode": errcode, "errmsg": errmsg})


appbuilder.add_view(UploadUserExcel,
                    "用户数据",
                    icon = "fa-cloud-upload",
                    category = '上传数据')

appbuilder.add_view(UploadBuildingExcel,
                    "物业数据",
                    icon = "fa-upload",
                    category = '上传数据')

appbuilder.add_view(UploadClientExcel,
                    "客户数据",
                    icon = "fa-arrow-up",
                    category = '上传数据')