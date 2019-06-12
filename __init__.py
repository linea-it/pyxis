from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['WTF_CSRF_SECRET_KEY'] = 'random key for form'
app.config['LDAP_PROVIDER_URL'] = 'ldap://ldap5.linea.gov.br/'
app.config['LDAP_PROTOCOL_VERSION'] = 3
db = SQLAlchemy(app)
 
app.secret_key = 'some_random_key'
 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
 
from pyxis.auth.views import auth
app.register_blueprint(auth)
 
db.create_all()

# from flask import Flask, Response, render_template, flash, session, request, redirect
# import os
# import datetime
# import jwt
# import ldap

# app = Flask(__name__)

# def ldap_auth(username, password):
#   ldap_server="ldap://ldap5.linea.gov.br"
#   user_dn = "uid="+username+",ou=people,dc=des-brazil,dc=org"
#   connect = ldap.initialize(ldap_server)

#   try:
#     connect.simple_bind_s(user_dn,password)
#     connect.unbind_s()
#     return True
#   except ldap.LDAPError:
#     connect.unbind_s()
#     return False

# def check_auth(username, password):
#     """This function is called to check if a username /
#     password combination is valid.
#     """
#     return ldap_auth(username, password)

# def authenticate():
#     """Sends a 401 response that enables basic auth"""
#     return Response(
#         'Could not verify your access level for that URL.\n'
#         'You have to login with proper credentials', 401,
#         {'WWW-Authenticate': 'Basic realm="Login Required"'})

# @app.route("/check")
# def check():
#     auth = request.authorization
#     if not auth or not check_auth(auth.username, auth.password):
#         return authenticate()
#     return Response('Login OK', 200, {})   

# if __name__ == '__main__':
#     app.secret_key = '29cSy004wj2931m'
#     app.run(port=os.environ.get('PORT', '7000'),
#             host=os.environ.get('HOST', '0.0.0.0'))
