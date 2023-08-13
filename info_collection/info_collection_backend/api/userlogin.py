from flask import jsonify, request
from flask_login import login_required, current_user
from api import app, db, login_manager, token_serializer,yzm_dict, img_dict
from . import vericode
from api.common import make_return, log
from app.models import UserTable
import hashlib
import random
import datetime
import re
import os
from io import BytesIO



#生成用户登录token
def generate_token(userid):
    app.logger.info('generate token for %s' % userid)
    data = {
        'userid': userid
    }
    token = token_serializer.dumps(data).decode('utf8')
    app.logger.info('generate token %s' % token)
    return token

#字符串MD5加密
def generate_MD5(opstr):
    MD5str = hashlib.md5()
    MD5str.update(opstr.encode("utf8"))
    return MD5str.hexdigest().upper()

#生成四位含数字和大小写字母的验证码
def generate_yzm():
    yzm = ""
    #range(x)生成x个随机数的验证码
    for i in range(4):    
        j = random.randrange(0,4) #跟随循环生成一个0-4之间的随机数来决定生成的是大小写字母还是数字  
        if j == 1:                #随机产生的数字是1时，生成数字
            a = random.randrange(0,10)
            yzm = yzm + str(a) 
        elif j == 2:              #随机产生的数字是2时，生成大写字母
            a = chr(random.randrange(65,91))
            yzm = yzm + a 
        else:                     #随机产生的数字是除了1和2时，生成小写字母
            a = chr(random.randrange(97,127))
            yzm = yzm + a
    return yzm


@login_manager.request_loader
def load_user(req):
    token = req.headers.get('token', None)
    if not token:
        app.logger.info('check token failed')
        return None
    try:
        data = token_serializer.loads(token)
        user = db.session.query(UserTable).filter(UserTable.id == data['userid']).first()
        if not user:
            app.logger.info('query user failed')
            return None
        else:
            return user
    except Exception:
        app.logger.info('check token failed')
        return None

@app.route('/')
def test():
    return make_return(True, generate_MD5('123456'))

#获取登录短信验证
@app.route('/user/get_sms_code', methods=['POST'])
def get_sms_code():
    try:
        json = request.json
        account = json.get('account') #账号
        password = json.get('password') #密码
        
        if account.strip()=='' or password.strip()=='':
            return make_return(False, '必填信息缺失！',data={})

        user = db.session.query(UserTable).filter(UserTable.phone_nbr == account).first()
        if not user:
            return make_return(False, '用户账号不存在！',data={})

        if user.password != generate_MD5(password):           
            return make_return(False, '用户密码错误！',data={}) 
    
        #生成验证码并保存到数据库
        newyzm = generate_yzm()
        yzm_dict[user.id]={'yzm':newyzm,'createtime':datetime.datetime.now(),'state':1}

        #发送验证码到用户手机
    
        return make_return(True, '验证码'+newyzm+'已发送到注册号码,请在10分钟内使用！')
    except Exception as ex:
        app.logger.error(str(ex))
        return make_return(False, "获取登录短信验证异常",data={})

@app.route('/login/generate_img', methods=['POST'])
def generate_img():
    try:
        json = request.json
        account = json.get('account') #账号
        f = BytesIO()
        code,image = vericode.veri_code()
        image.save(f,'jpeg')
        # 二进制流
        img_stream = f.getvalue()
        import base64
        img_stream = base64.b64encode(img_stream)

        img_dict[account] = {'yzm':code,'createtime':datetime.datetime.now(
            ),'state':1}
        print(img_dict)
        return make_return(True, "成功",data={'img_stream':img_stream})
    except Exception as ex:
        app.logger.error(str(ex))
        app.logger.exception(ex)
        return make_return(False, "获取登录验证图片异常",data={})


#用户提交用户信息并登录
@app.route('/user/login', methods=['POST'])
def login():
    try:
        json = request.json
        account = json.get('account') #账号
        password = json.get('password') #密码
        sms_code = json.get('sms_code') #验证码
        random_token = json.get('random_token')

        yzm =  img_dict[account]

        if not yzm:
            return make_return(False, '无可用验证码，请先获取！',data={})

        if yzm['yzm'] != sms_code:
            return make_return(False, '验证码错误！',data={})

        if yzm['state']!=1 or yzm['createtime']<datetime.datetime.now(
            )-datetime.timedelta(minutes=10):
            return make_return(False, '验证码失效，请重新获取！',data={})

        #验证通过，验证码失效
        img_dict[account]['state'] = 0

        if account.strip()=='' or password.strip()=='' or sms_code.strip()=='':
            return make_return(False, '必填信息缺失！',data={})

        user = db.session.query(UserTable).filter(UserTable.phone_nbr == account).first()
        if not user or user.password != generate_MD5(password):
            return make_return(False, '用户账号或密码错误！',data={})

        regex = re.compile(r'^(?=.*[0-9])(?=.*[a-zA-Z])(?=([\x21-\x7e]+)[^a-zA-Z0-9]).{8,20}$')
        if not regex.match(password):
            return make_return(True, 
                '密码强度不足，密码必须包含字母（大写或小写）、数字和特殊符号的组合,至少8个字符，\
                最多20个字符，请按要求修改！',
                data={'token': generate_token(user.id),
                'message':'密码强度不足!'})
        else:
            return make_return(True,'用户验证成功，登录完成！',
                data={'token': generate_token(user.id),'message':'用户验证成功，登录完成！'})
    except Exception as ex:
        app.logger.error(str(ex))
        app.logger.exception(ex)
        return make_return(False, "用户登录验证异常！",data={})

#用户密码修改
@app.route('/user/changepassword', methods=['POST'])
@login_required
def changepassword():
    try:
        json = request.json
        old_password = json.get('old_password') #原密码
        new_password = json.get('new_password') #新密码
        confirm_password = json.get('confirm_password') #新密码重复

        user = load_user(request)
        #user = db.session.query(userlist).filter(userlist.user_name == 'test').first()
        if not user:
            return make_return(False, '用户未登录或不存在，请重新登录！',data={})

        if old_password.strip()=='' or old_password.strip()=='' or old_password.strip()=='':
            return make_return(False, '必填信息缺失！',data={})

        if user.password != generate_MD5(old_password):
            return make_return(False, '用户旧密码错误！',data={}) 
        
        if old_password == new_password:
            return make_return(False, '新密码不可与旧密码一样！',data={}) 
        
        if new_password != confirm_password:
            return make_return(False, '两次输入的新密码不一致！',data={}) 
        
        regex = re.compile(r'^(?=.*[0-9])(?=.*[a-zA-Z])(?=([\x21-\x7e]+)[^a-zA-Z0-9]).{8,20}$')
        if not regex.match(new_password):
            return make_return(False, 
                '新密码强度不足，密码必须包含字母（大写或小写）、数字和特殊符号的组合,至少8个字符，\
                最多20个字符，请按要求修改！',data={}) 
        else:
            user.password = generate_MD5(new_password);  
            db.session.merge(user)   
            db.session.commit()
        
            return make_return(True, '密码修改完毕！',data={})
    except Exception as ex:
        app.logger.error(str(ex))
        return make_return(False, "用户密码修改异常！",data={})


#用户信息及统计信息显示
@app.route('/user/info', methods=['GET'])
@login_required
def info():
    try:
        user = load_user(request)
        #user = db.session.query(userlist).filter(userlist.user_name == 'cs01').first()
        if not user:
            return make_return(False, '用户未登录或不存在，请重新登录！',data={})
        
        tinfo = db.session.query(UserTable).filter(UserTable.user_name == user.user_name).first()
        # tinfo = db.engine.execute(
        #     "select * from sla_user_tj where user_name='"+user.user_name+"'").first()
        if not tinfo:
            return make_return(False, '未查到用户统计数据！',data={})

        tdata = {
            'name':tinfo.user_name,
            'phone':tinfo.phone_nbr,
            'user_dept':tinfo.user_dept,
            'contractor_group':tinfo.contractor_group
        }
        
        return make_return(True, '提取完毕！',data=tdata)

    except Exception as ex:
        app.logger.error(str(ex))
        return make_return(False, "提取用户信息异常！",data={})




