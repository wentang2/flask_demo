#coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy # database


# 登录
import os
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir

# 邮件
from config import basedir, ADMINS, MAIL_SERVER, MAIL_POST, MAIL_USERNAME, MAIL_PASSWORD


# 创建app应用程序
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)



# 登录配置
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login' #允许登录时，重定向到的视图
oid = OpenID(app, os.path.join(basedir,'tmp')) # openid 扩展 在tmp里存储临时文件

# login
from app import views, models



# 邮件 使用python logging 模块，当发生异常的时候发送邮件
# if not app.debug:
#     import logging
#     from logging.handlers import SMTPHandler
#     credentials = None 
#     if MAIL_USERNAME or MAIL_PASSWORD:
#         credentials = (MAIL_USERNAME, MAIL_PASSWORD)
#     mail_handler = SMTPHandler((MAIL_SERVER,MAIL_POST), 'no-reply@' + MAIL_SERVER, ADMINS, 'Hello failure', credentials)
#     mail_handler.setLevel(logging.ERROR)
#     app.logger.addHandler(mail_handler)


# 启用日志记录类似于电子邮件发送错误
if not app.debug:
    import logging
    from logger.handlers import RotatingFileHandler
    # 日志文件保存在tmp目录，叫 microblog.log。 rotatingfilehandler限制日志大小为1M，保留最后10个文件
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    # logging.formatter 定制化日志信息格式， 时间戳、日志记录级别、消息起源于以及日志消息和堆栈跟踪的文件和行号
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)   #设置日志级别为 info
    file_handler.setLevel(loggin.INFO)
    app.logger.addHandler(file_handler) # 添加一个handler
    app.logger.info('microblog startup')