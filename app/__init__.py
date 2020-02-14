#coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy # database


import os
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)




lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login' #允许登录时，重定向到的视图
oid = OpenID(app, os.path.join(basedir,'tmp')) # openid 扩展 在tmp里存储临时文件

# login
from app import views, models