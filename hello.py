from flask import Flask,render_template,request,redirect,url_for
import re
from flask_sqlalchemy import SQLAlchemy
import os
from flask import request,jsonify
basedir = os.path.abspath(os.path.dirname(__file__))
App=Flask(__name__)
App.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
App.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
App.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(App)
#post RFID卡的信息
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

#get RFID卡的信息
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
###########################################################################
#post UserInfo的信息
@App.route('/postUser',methods=['POST'])
def postUser():
	user_id=request.form['user_id']
	user_name=request.form['user_name']
	phone_num=request.form['phone_num']
	score=request.form['score']
	userinfo=UserInfo(user_id=user_id,
						user_name=user_name,
						phone_num=phone_num,
						score=score)
	db.session.add(userinfo)
	db.session.commit()
	return 'post success',200
#get UserInfo的信息
@App.route('/getUser/<user_id>',methods=['GET'])
def getUser(user_id):
	user=UserInfo.query.filter_by(user_id=user_id).first()
	if user:
		return jsonify({'user_id':user.user_id,
						'user_name':user.user_name,
						'phone_num':user.phone_num,
						'score':user.score})
	else:
		return 'not found',404
###########################################################################
#post ScoreInfo的信息
@App.route('/postScore',methods=['POST'])
def postScore():
	record_id=request.form['record_id']
	card_id=request.form['card_id']
	score_change=request.form['score_change']
	change_time=request.form['change_time']
	operator=request.form['operator']
	userinfo=ScoreInfo(record_id=record_id,
						card_id=card_id,
						score_change=score_change,
						change_time=change_time,
						operator=operator)
	db.session.add(userinfo)
	db.session.commit()
	return 'post success',200
#get ScoreInfo的信息
@App.route('/getScore/<record_id>',methods=['GET'])
def getScore(record_id):
	records=ScoreInfo.query.filter_by(record_id=record_id).all()
	if records:
		a=list()
		for item in records:
			a.append({'record_id':item.record_id,
					'card_id':item.card_id,
					'score_change':item.score_change,
					'change_time':item.change_time,
					'operator':item.operator})
		return jsonify({'records':a})
	else:
		return 'not found',404
###########################################################################
###########################################################################
###########################################################################
###########################################################################
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
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
class RfidCard(db.Model):
	__tablename__='rfidcard'
	id=db.Column(db.Integer,primary_key=True)
	card_id=db.Column(db.String(64),unique=True)
	user_id=db.Column(db.String(64),unique=True)
	card_time=db.Column(db.String(64))
	freeze=db.Column(db.String(64))
	def __repr__(self):
		return '<RfidCard %r>'%self.name
#用户：身份证号码/姓名/电话/积分
class UserInfo(db.Model):
	__tablename__='userinfo'
	id=db.Column(db.Integer,primary_key=True)
	user_id=db.Column(db.String(64),unique=True)
	user_name=db.Column(db.String(64))
	phone_num=db.Column(db.String(64))
	score=db.Column(db.String(64))
	def __repr__(self):
		return '<RfidCard %r>'%self.name
#积分变动记录：记录编号/卡号/变动时间/变动积分/操作员
class ScoreInfo(db.Model):
	__tablename__='scoreinfo'
	id=db.Column(db.Integer,primary_key=True)
	record_id=db.Column(db.String(64),unique=True)
	card_id=db.Column(db.String(64))
	change_time=db.Column(db.String(64))
	score_change=db.Column(db.String(64))
	operator=db.Column(db.String(64))
	def __repr__(self):
		return '<RfidCard %r>'%self.name
if __name__=='__main__':
    App.run(debug=True)

