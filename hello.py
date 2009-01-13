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
#post 修改
@App.route('/PostData',methods=['POST'])
def postData():
	eastLongitude=request.form['eastLongitude']
	northLatitude=request.form['northLatitude']
	depth=request.form['depth']
	torque=request.form['torque']
	rotationalSpeed=request.form['rotationalSpeed']
	time=request.form['time']
	data=MachineParameters(eastLongitude,northLatitude,depth,torque,rotationalSpeed,time)
	db.session.add(data)
	db.session.commit()
	return 'success',200
	#get 修改冻结
@App.route('/getData',methods=['GET'])
def getData():
	query2=MachineParameters.query
	datas=query2.offset(query2.count()-50)
	if datas:
		a=list()
		for data in datas:
			a.append({'eastLongitude':data.eastLongitude,
						'northLatitude':data.northLatitude,
						'depth':data.depth,
						'torque':data.torque,
						'rotationalSpeed':data.rotationalSpeed,
						'time':data.time})
		return jsonify({'datas':a})
	else:
		return 'not found',404
@App.route('/addData/<time>',methods=['GET'])
def addData(time):
	data=MachineParameters(eastLongitude='eastLongitude',northLatitude='northLatitude',depth='depth',torque='torque',rotationalSpeed='rotationalSpeed',time=time)
	db.session.add(data)
	db.session.commit()
	return 'success',200
###########################################################################
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
class MachineParameters(db.Model):
	__tablename__='MachineParameters'
	id=db.Column(db.Integer,primary_key=True)
	eastLongitude=db.Column(db.String,unique=False)
	northLatitude=db.Column(db.String,unique=False)
	depth=db.Column(db.String,unique=False)
	torque=db.Column(db.String,unique=False)
	rotationalSpeed=db.Column(db.String,unique=False)
	time=db.Column(db.String,unique=False)
	def __repr__(self):
		return '<MachineParameters %r>'%self.name
if __name__=='__main__':
    App.run(debug=True)

