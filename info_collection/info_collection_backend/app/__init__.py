import logging
import json
import logging.config
from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from .MyIndexView import MyIndexView
from itsdangerous import TimedJSONWebSignatureSerializer
from flask_cors import CORS
from flask_login import LoginManager
from .MySecurityManager import MySecurityManager


"""
 Logging configuration
"""

# logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
# logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)
appbuilder = AppBuilder(app, db.session, indexview=MyIndexView, security_manager_class=MySecurityManager)
# appbuilder = AppBuilder(app, db.session, indexview=MyIndexView)

db.create_all()

"""
加载日志配置, 在代码中直接调用 logging.info(msg) 等方法即可输出日志
>>> app.logger.info('info msg') # 普通日志，在控制台和 logs/info.log 中输出
>>> app.logger.error('error msg') # 错误日志, 在控制台和 logs/error.log 中输出
"""


from app import views
