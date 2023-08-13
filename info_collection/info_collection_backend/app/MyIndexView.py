from flask_appbuilder import IndexView, expose
from flask import redirect, g, request

class MyIndexView(IndexView):

    @expose('/')
    def index(self):
        if not g.user.is_authenticated:
            return redirect(self.appbuilder.get_url_for_login)
        else:
            return super(MyIndexView, self).index()