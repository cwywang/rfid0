from flask import Flask,render_template,request,redirect,url_for
import re
from flask_sqlalchemy import SQLAlchemy
import os
from flask import request,jsonify
basedir = os.path.abspath(os.path.dirname(__file__))
#from send_mail import Send_Mail
App=Flask(__name__)
App.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
App.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
App.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(App)
#mail=Send_Mail('system@email.doforyou.gift','Aa741077081')
@App.route('/postCard',methods=['POST'])
def postCard():
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
@App.route('/getCard/<card_id>',methods=['GET'])
def getCard(card_id):
	card=RfidCard.query.filter_by(card_id=card_id).first()
	if card:
		return jsonify({'card_id':card.card_id,
						'user_id':card.user_id,
						'card_time':card.card_time,
						'freeze':card.freeze})
	else:
		return 'not found',404
@App.route('/addCard',methods=['GET'])
def addCard():
	rfidcard=RfidCard(card_id="card_id",
						user_id="user_id",
						card_time="card_time",
						freeze="freeze")
	db.session.add(rfidcard)
	db.session.commit()
	return "123",200
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