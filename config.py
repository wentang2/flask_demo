#coding=utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(basedir,'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,'db_repository')
#
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    { 'name': 'myopenid', 'url': 'https://www.myopenid.com' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'http://wentang.openid.org.cn/' }]

# mail server settings
MAIL_SERVER = 'localhost'
MAIL_POST = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None 

# administrator list
ADMINS = ['lvxinqiang2@163.com']