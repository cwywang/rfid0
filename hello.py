from flask import Flask,render_template,request,redirect,url_for
import re
from flask_sqlalchemy import SQLAlchemy
import os
basedir = os.path.abspath(os.path.dirname(__file__))
#from send_mail import Send_Mail
App=Flask(__name__)
App.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
App.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db=SQLAlchemy(App)
#mail=Send_Mail('system@email.doforyou.gift','Aa741077081')
@App.route('/rfidcard',methods=['POST'])
def rfidcard():
	card_id=request.form['card_id']
	user_id=request.form['user_id']
	card_time=request.form['card_time']
	freeze=request.form['freeze']
	rfidcard=RfidCard(card_id=card_id,
						user_id=user_id,
						card_time=card_time,
						freeze=freeze)
	db.session.add(rfidcard)
	db.session.commit()
	return 'post success',200
@App.route('/card1',methods=['GET'])
def card1():
	rfidcard=RfidCard(card_id="card_id",
						user_id="user_id",
						card_time="card_time",
						freeze="freeze")
	db.session.add(rfidcard)
	db.session.commit()
	return "123",200
@App.route('/card',methods=['GET'])
def card():
	Rcard=RfidCard.query.filter_by(card_id="card_id").first()
	return Rcard.card_id+"123",200
@App.route('/init',methods=['GET'])
def init():
	db.drop_all()
	db.create_all()
	return "ok"
class RfidCard(db.Model):
	__tablename__='rfidcard'
	id=db.Column(db.Integer,primary_key=True)
	card_id=db.Column(db.String(64),unique=True)
	user_id=db.Column(db.String(64),unique=True)
	card_time=db.Column(db.String(64))
	freeze=db.Column(db.String(64))
	def __repr__(self):
		return '<RfidCard %r>'%self.name
if __name__=='__main__':
    App.run(debug=True)