from flask import g, jsonify, request, redirect, flash
from flask_appbuilder import expose
from flask_appbuilder.security.views import AuthView
from flask_appbuilder.security.forms import LoginForm_db
from flask_login import login_user
import requests
import random
import datetime

login_sms_dict = {}

class AuthDBView(AuthView):
    login_template = "login_db.html"

    @expose("/login/", methods=["GET", "POST"])
    def login(self):
        if g.user is not None and g.user.is_authenticated:
            return redirect(self.appbuilder.get_url_for_index)
        form = LoginForm_db()
        if form.validate_on_submit():
            sms_code = request.form.get('sms')
            # verify sms from request params with global dict
            # 1. same sms 2. this_send_time-send_time>60s
            same_sms = login_sms_dict[int(form.username.data)][0]==sms_code
            delta_time = datetime.datetime.now() - login_sms_dict[int(form.username.data)][1]
            if same_sms and delta_time.seconds<60:
                # remove user sms info dict key:value pair
                del login_sms_dict[int(form.username.data)]

                user = self.appbuilder.sm.auth_user_db(
                    form.username.data, form.password.data
                )
                if not user:
                    flash(as_unicode(self.invalid_login_message), "warning")
                    return redirect(self.appbuilder.get_url_for_login)
                login_user(user, remember=False)
                return redirect(self.appbuilder.get_url_for_index)
            else:
                flash(('验证码已失效，请重新发送！'), "warning")
                return redirect(self.appbuilder.get_url_for_login)
        return self.render_template(
            self.login_template, title=self.title, form=form, appbuilder=self.appbuilder
        )

    @expose("/sms_generate", methods=["GET", "POST"])
    def sms_generate(self):
        if g.user is not None and g.user.is_authenticated:
            return redirect(self.appbuilder.get_url_for_index)
        form = LoginForm_db()
        if form.validate_on_submit():
            # check this_send_time-send_time>60s
            usn= int(form.username.data)
            delta_time = login_sms_dict[usn][1]-datetime.datetime.now() if usn in login_sms_dict else None
            if delta_time is None or delta_time.seconds > 60:
                user = self.appbuilder.sm.auth_user_db(
                    form.username.data, form.password.data
                )
                if not user:
                    flash(as_unicode(self.invalid_login_message), "warning")
                    return redirect(self.appbuilder.get_url_for_login)
                else:
                    # send sms                
                    proxies = {
                      "http": "http://x.x.x.x:8080",
                      "https": "http://x.x.x.x:8080",
                    }
                    to = int(form.username.data)
                    content = str(random.randint(100000,999999))
                    print('您的验证码是： '+content)
                    param = {'username':'xxx','password':'xxx',
                        'to':to,'content':'您的验证码是：  '+content}
                    r=requests.get("http://gatewayxxxx.xx/GsmsHttp",
                        params=param, proxies=proxies)
                    # store sms code to the global dict {user:[pass,send_time]}
                    login_sms_dict[to]=[content, datetime.datetime.now()]
                    return jsonify({"errcode": 0, "errmsg": '验证码发送成功！'})
            else:
                # return error msg
                return jsonify({"errcode": 1, "errmsg": '请在60秒后再次发送验证码！'})
        return self.render_template(
            self.login_template, title=self.title, form=form, appbuilder=self.appbuilder
        )