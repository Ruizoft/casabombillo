from flask import Flask, render_template,flash, g, session, redirect, url_for
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine
app = Flask(__name__)
app.config.from_object('config')
Session = sessionmaker()
#engine = create_engine('mysql+mysqldb://root:Iltzm1013@localhost/casabombillo')
engine = create_engine('mysql+mysqldb://root@/bombillo', connect_args={'unix_socket':'/cloudsql/casabombillo:admin'})
Session.configure(bind=engine)

sess = Session()
Base = declarative_base()


from app.adminModule.controllers import  mod_auth as auth_module

app.register_blueprint(auth_module)

@app.route('/')
def welcome():
	return render_template("welcome.html")


#@app.route('/main')
#def main():
	#return render_template("main.html")
