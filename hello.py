from flask import Flask,render_template,request,redirect,url_for
import re
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os
from flask import request,jsonify
basedir = os.path.abspath(os.path.dirname(__file__))
App=Flask(__name__)
App.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
App.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
App.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(App)
bootstrap=Bootstrap(App)
#post 修改积分
@App.route('/changeScore',methods=['POST'])
def changeScore():
	user_id=request.form['user_id']
	score=request.form['score']
	user=UserInfo.query.filter_by(user_id=user_id).first()
	if user:
		user.score=score
		db.session.add(user)
		db.session.commit()
		return 'post success',200
	else:
		return "not found",404
#post 修改冻结
@App.route('/freezeCard',methods=['POST'])
def freezeCard():
	card_id=request.form['card_id']
	freeze=request.form['freeze']
	card=RfidCard.query.filter_by(card_id=card_id).first()
	if card:
		card.freeze=freeze
		db.session.add(card)
		db.session.commit()
		return 'post success',200
	else:
		return "not found",404
#post RFID卡的信息
@App.route('/postCard',methods=['POST'])
def postCard():
	card_id=request.form['card_id']
	user_id=request.form['user_id']
	card_time=request.form['card_time']
	freeze=request.form['freeze']
	card=RfidCard.query.filter_by(card_id=card_id).first()
	if card:
		return 'not found',404
	else:
		card=RfidCard(card_id=card_id,
					user_id=user_id,
					card_time=card_time,
					freeze=freeze)
	db.session.add(card)
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
		return 'not found',200
###########################################################################
#post UserInfo的信息
@App.route('/postUser',methods=['POST'])
def postUser():
	user_id=request.form['user_id']
	user_name=request.form['user_name']
	phone_num=request.form['phone_num']
	score=request.form['score']
	userinfo=UserInfo.query.filter_by(user_id=user_id).first()
	if userinfo:
		return "not found",404
	else:
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
	card_id=request.form['card_id']
	score_change=request.form['score_change']
	change_time=request.form['change_time']
	userinfo=ScoreInfo(card_id=card_id,
						score_change=score_change,
						change_time=change_time)
	db.session.add(userinfo)
	db.session.commit()
	return 'post success',200
#get ScoreInfo的信息
@App.route('/getScore/<card_id>',methods=['GET'])
def getScore(card_id):
	records=ScoreInfo.query.filter_by(card_id=card_id).all()
	if records:
		a=list()
		for item in records:
			a.append({'card_id':item.card_id,
					'score_change':item.score_change,
					'change_time':item.change_time})
		return jsonify({'records':a})
	else:
		return 'not found',200
###########################################################################
###########################################################################
###########################################################################
#管理界面
@App.route('/manage/<func>',methods=['GET'])
def manage(func):
	if func=="card":
		cards=RfidCard.query.filter_by().all()
		return render_template("manage_card.html",cards=cards)
	if func=="user":
		users=UserInfo.query.filter_by().all()
		return render_template("manage_user.html",users=users)
	if func=="score":
		scores=ScoreInfo.query.filter_by().all()
		return render_template("manage_score.html",scores=scores)
	if func=="home":
		return render_template("manage.html")
	return "没得了...",404
###########################################################################
@App.route('/addCard/<card_id>',methods=['GET'])
def addCard(card_id):
	card=RfidCard(card_id=card_id,
					user_id="user_id",
					card_time="card_time",
					freeze="freeze")
	db.session.add(card)
	db.session.commit()
	return card_id,200
@App.route('/addUser/<user_id>',methods=['GET'])
def addUser(user_id):
	user=UserInfo(user_id=user_id,
					user_name="user_name",
					phone_num="phone_num",
					score="score")
	db.session.add(user)
	db.session.commit()
	return user_id,200
@App.route('/addScore/<card_id>',methods=['GET'])
def addScore(card_id):
	score=ScoreInfo(card_id=card_id,
					change_time="change_time",
					score_change="score_change")
	db.session.add(score)
	db.session.commit()
	return card_id,200
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
	user_id=db.Column(db.String(64))
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
#积分变动记录：卡号/变动时间/变动积分
class ScoreInfo(db.Model):
	__tablename__='scoreinfo'
	id=db.Column(db.Integer,primary_key=True)
	card_id=db.Column(db.String(64))
	change_time=db.Column(db.String(64))
	score_change=db.Column(db.String(64))
	def __repr__(self):
		return '<RfidCard %r>'%self.name
if __name__=='__main__':
    App.run(debug=True)

