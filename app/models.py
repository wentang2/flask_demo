# coding=utf-8
from app import db
from hashlib import md5

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140)) #增加的自我介绍
    last_seen = db.Column(db.DateTime)  # 增加的最后访问时间

    @property
    def is_authenticated(self): # 身份通过验证
        return True

    @property
    def is_active(self):   
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):   #返回用户数据库中的ID
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3
    
    #
    def avatar(self, size): # 头像
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)
    

    # 创建一个新的唯一名字 如果已存在重复名字，则加后缀为2、3等等
    @staticmethod   # 静态方法，这个操作与任何实例都无关
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() == None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() == None:
                break
            version += 1
        return new_nickname

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)