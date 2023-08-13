from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, AppBuilder, expose, BaseView, has_access
from app import appbuilder, db
from app.models import OrderStatusTable, service_request
from flask_appbuilder.models.sqla.filters import FilterNotEqual

class ServiceChangeView(ModelView):
    datamodel = SQLAInterface(OrderStatusTable)
    list_title = '装机回单列表'
    base_filters = [['ordertype', FilterNotEqual, '6'], ['ordertype', FilterNotEqual, '7'], ['status',FilterNotEqual, 'C']]
    label_columns = {'CO':'CO', 'serialuserid':'SO', 'appl_date': '受理时间', \
                    'send_date':'发送时间','work_area': '装机公司', 'return_date':'回单时间'}
    list_columns = ['CO', 'serialuserid', 'work_area', 'appl_date', 'send_date', 'return_date']

class ServiceRequestView(ModelView):
    datamodel = SQLAInterface(service_request)
    list_title = '故障回单列表'
    label_columns = {'serialuserid':'故障单号', 'last_modify_time': '最后修改时间', 'location':'地址', \
                    'finish_status':'回单状态'}
    list_columns = ['serialuserid', 'location', 'last_modify_time', 'finish_status']


db.create_all()


appbuilder.add_view(ServiceChangeView,
                    "装机回单",
                    icon = "fa-envelope",
                    category = "回单状态")
appbuilder.add_view(ServiceRequestView,
                    "故障回单",
                    icon = "fa-folder-open-o",
                    category = "回单状态")
