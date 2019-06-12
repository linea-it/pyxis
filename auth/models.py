import ldap
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired
from pyxis import db, app
 
fake_users = [
    {'username': 'singulani', 'password': '12345'},
    {'username': 'zeze', 'password': '00000'}
]


def get_ldap_connection():
    conn = ldap.initialize(app.config['LDAP_PROVIDER_URL'])
    return conn
 
 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
 
    def __init__(self, username, password):
        self.username = username
 
    @staticmethod
    def try_login(username, password):
        #conn = get_ldap_connection()
        #conn.simple_bind_s(
        #    "uid="+username+",ou=people,dc=des-brazil,dc=org",
        #    password
        #)

        for user in fake_users:
            print(user)
            if user.get('username') == username and user.get('password') == password:
                return True

        raise ldap.INVALID_CREDENTIALS

 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return self.id
 
 
class LoginForm(Form):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])