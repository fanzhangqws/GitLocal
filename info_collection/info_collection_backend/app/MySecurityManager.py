from flask_appbuilder.security.sqla.manager import SecurityManager
from .New_AuthDBView import AuthDBView

login_sms_dict = {}

class MySecurityManager(SecurityManager):
    authdbview = AuthDBView