from flask import current_app
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Hosts(db.Model):

    __tablename__ = 'hosts'

    id = db.Column(db.Integer,primary_key=True)
    netip = db.Column(db.String(64),unique=True,nullable=True)
    name = db.Column(db.Text,nullable=True)
    area = db.Column(db.String(64),nullable=True)
    internet = db.Column(db.String(64),nullable=True)
    cpuinfo = db.Column(db.String(64),nullable=True)
    memory = db.Column(db.String(64),nullable=True)


class Groupname(db.Model):

    __tablename__ = 'groupname'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False,unique=True)
    comment = db.Column(db.Text)

class Grouphostid(db.Model):

    __tablename__ = 'grouphostid'

    id = db.Column(db.Integer,primary_key=True)
    groupid = db.Column(db.Integer)
    hostid = db.Column(db.Integer)

class datastore(db.Model):

    __tablename__ = 'datastore'

    id = db.Column(db.Integer, primary_key=True)
    netip = db.Column(db.String(128),unique=False,nullable=True)
    port = db.Column(db.String(64),nullable=True)
    cpu = db.Column(db.String(64),nullable=True)
    memory = db.Column(db.String(64),nullable=True)
    name = db.Column(db.Text,nullable=True)
    area = db.Column(db.String(64),nullable=True)
    types = db.Column(db.String(64),nullable=True)
    version = db.Column(db.String(64),nullable=True)
    connect_number = db.Column(db.String(64),nullable=True)



class User(UserMixin,db.Model):
    
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(128),unique=True)
    passwd_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    status = db.Column(db.Boolean, default=False)
    last_time = db.Column(db.DateTime, default=datetime.now)
    roles = db.Column(db.String(128), nullable=True)
    rolesid = db.Column(db.String(128), nullable=True)

    def ping(self):
        self.last_time = datetime.now()
        db.session.add(self)

    def tokens(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
	return s.dumps({'id':self.id})

    def loosen_tokens(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            userid = s.loads(token)
        except:
	    return False
        if userid.get('id') != self.id:
            return False
        self.status = True
	db.session.add(self)
	return True

    @staticmethod
    def reset_passwd_tokens(token,newpass):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            userid = s.loads(token)
        except: 
            return False
        user = User.query.get(userid.get('id'))
        if user is None:
	    return False
        user.password = newpass
        db.session.add(user)
        return True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.passwd_hash = generate_password_hash(password)

    def verify_passwd(self,password):
        return check_password_hash(self.passwd_hash, password)

class Menu(UserMixin,db.Model):

    __tablename__ = 'menus'
    
    id = db.Column(db.Integer,primary_key=True)
    submenuId = db.Column(db.Integer)
    name = db.Column(db.String(64))
    url = db.Column(db.String(128))
    level = db.Column(db.Integer)
    flag = db.Column(db.Integer)

class Tasks(UserMixin,db.Model):

    __tablename__ = "tasks"

    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(64))
    area = db.Column(db.String(64))
    types = db.Column(db.String(64))
    version = db.Column(db.String(64))
    dates = db.Column(db.DateTime)

class Filename(UserMixin,db.Model):
    
    __tablename__ = "filename"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)

class Logs(UserMixin,db.Model):

    __tablename__ = "logs"

    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(64))
    address = db.Column(db.String(64))
    datetime = db.Column(db.DateTime)
    strs = db.Column(db.String(128))

class Role(UserMixin,db.Model):

    __tablename__ = "roles"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    permission = db.Column(db.Text)
