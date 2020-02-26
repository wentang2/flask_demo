#coding=utf-8
from app import app, db, oid, lm
from flask import render_template, flash, redirect, session, g, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm, EditForm
from .models import User
from datetime import datetime   

@app.route('/')
@app.route('/index')
@login_required #只有登录用户可以看到内容，否则跳转到登录页（判断是否已登录）
def index():
    user = g.user
    posts = [ # fake array of posts
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
        title= 'Home',
        user = user,
        posts = posts)

# 登录
@app.route('/login',methods = ['GET','POST'])
@oid.loginhandler   #告诉flask-openid 以下是登录视图函数
def login():
    print '------login()--------'
    if g.user is not None and g.user.is_authenticated:    # g.user 是登录用户存储， 检查是否该用户已被认证（已登录）
        return redirect(url_for('index'))   #   已登录过的用户直接去首页
        print '--------index -------'
    form = LoginForm()
    if form.validate_on_submit():
        print '-------- form valid submit ------'
        session['remember_me'] = form.remember_me.data
        print '------openid: ',form.openid.data 
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    print '------login',g.user.is_authenticated, g.user.get_id()
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

# Flask-OpenID  登录回调  flask-openid认证成功后，调用一个装饰了oid.after_login的函数。失败则返回登陆界面
@oid.after_login
def after_login(resp):  #resp包含了openid提供商返回来的信息
    print '--------------after  login ----------'
    if resp.email is None or resp.email == "":      #判断邮箱 合法性
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()   #判断邮箱是否在数据库，不在则是新用户，添加进数据库
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_unique_nickname(nickname) # 让User类为我们选择一个唯一的名字。
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)   #注册本次有效登录
    return redirect(request.args.get('next') or url_for('index'))

#  用户加载回调
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

# g.user 全局变量 用来保存当前用户 方便接下来的请求进行验证
@app.before_request # 每次浏览器在发送请求之前被调用
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.now()  
        db.session.add(g.user)
        db.session.commit()
        print '---------before_request()-------'
        # print db.session.add()

# 登出
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# 用户信息页
@app.route('/user/<nickname>')
@login_required
def user(nickname):
    print '-------User---------'
    print session   #session是个字典，本质是本地加密钥的cookie
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    posts = [
        { 'author': user, 'body': 'Test post #1' },
        { 'author': user, 'body': 'Test post #2' }
    ]
    return render_template('user.html',
        user = user,
        posts = posts)

# 编辑功能，仅登录用户
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)  # add可以进行添加或者更新
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)

# 测试 url 唯一性
# 当访问 '/project' 时，会重定向到'/project/' 访问两个都有效
@app.route('/projects/')    # 结尾带 '/' 
def projects():
    return 'The project page'

# 只能访问 '/about' 。如果访问 '/about/'会 报404 not found
# 避免搜索引擎引同一个页面两次
@app.route('/about')        #结尾不带 '/'
def about():
    return 'The about page'


# 定制HTTP错误处理器 404 500
@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()   #如果错误是数据库触发，那么数据库会话是不正常的，需要回滚
    return render_template('500.html'), 500