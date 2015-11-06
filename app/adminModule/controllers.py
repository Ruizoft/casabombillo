from app.adminModule.models import User
from app import sess
from sqlalchemy.dialects.mysql import mysqldb
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash
from oauth2client import client, crypt
import json



mod_auth = Blueprint('auth', __name__)
CLIENT_ID = "52982340847-0ese8t6k4tstva6412htlekat6cp78it.apps.googleusercontent.com"
WEB_CLIENT_ID = "52982340847-0ese8t6k4tstva6412htlekat6cp78it.apps.googleusercontent.com"
APPS_DOMAIN_NAME = "http://localhost:8080"


@mod_auth.route('/admin/login', methods=['GET', 'POST'])
def adminLogin():
	form = request.form
	if form:
		email = form['email']
		password = form['password']
		user = sess.query(User).filter(User.email == email).first()
		if user and check_password_hash(user.password, password):

			session['user_id'] = user.id

			flash('Welcome %s' % user.name)

			return redirect(url_for('auth.adminMain'))

		flash('El correo o contrasena no son validos', 'error-message')

	return render_template("admin-login.html")  

@mod_auth.route('/admin/main', methods=['GET', 'POST'])
def adminMain():
	form = request.form
	if 'user_id' in session:
		return render_template("admin-main.html")
	return redirect(url_for('auth.adminLogin'))


@mod_auth.route('/admin/register', methods=['GET', 'POST'])
def register():
	if 'user_id' in session:
	    form = request.form
	    if form:
	        email = form['email']
	        password = form['password']
	        user = sess.query(User).filter(User.email == email).first()

	        if user and check_password_hash(user.password, password):

	            flash('Usuario ya creado', 'error-message')
	            return render_template("admin-register.html")

	        user = User(form['name'], form['email'], generate_password_hash(form['password']))
	        sess.add(user)
	        sess.commit()
	        return redirect(url_for("auth.adminMain"))

	    return render_template("admin-register.html")
	return redirect(url_for('auth.adminLogin'))  

@mod_auth.route('/signout', methods=['GET', 'POST'])
def signout():
	if 'user_id' in session:
		session.pop('user_id', None)
		session.pop('guid', None)
		
	return redirect(url_for('auth.signin'))

@mod_auth.route('/gSignin', methods=['POST'])
def gSignin():
	token = request.data
	try:
	    idinfo = client.verify_id_token(token, CLIENT_ID)
	    if idinfo['aud'] not in [WEB_CLIENT_ID]:
	        raise crypt.AppIdentityError("Unrecognized client.")
	    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
	        raise crypt.AppIdentityError("Wrong issuer.")
	except crypt.AppIdentityError:
		return json.dumps('No se pudo ingresar al sistema')

	userid = idinfo['sub']
	user = sess.query(User).filter(User.guid == userid).first()
	if user != None:

		session['user_id'] = user.id
		session['guid'] = user.guid
		session['gfolder'] = user.gfolder

		flash('Bienvenido %s' % user.name)

		return json.dumps("%s" % user.name)
	else:
		session['error'] = "eroor"
		return redirect(url_for('auth.signin'))
