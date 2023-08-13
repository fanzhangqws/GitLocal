from flask import Flask
from flask_appbuilder import SQLA
from itsdangerous import TimedJSONWebSignatureSerializer
from flask_cors import CORS
from flask_login import LoginManager


"""
 Logging configuration
"""

# logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
# logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)

db.create_all()

yzm_dict = {}
img_dict = {}

# 跨域请求支持
CORS(app)

# 登录管理器支持
login_manager = LoginManager()
login_manager.init_app(app)

# jwt(token)生成器
TOKEN_SECRET = 'I1bz5QwNn5ZPpXpEUrju5hsmZQrhZ196'  # token 密钥
token_serializer = TimedJSONWebSignatureSerializer(
    TOKEN_SECRET, expires_in=3600 * 24)

import api.userlogin
import api.infocollect