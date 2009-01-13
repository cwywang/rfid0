from . import db
#RFID卡：卡号/用户编号/发卡时间/是否冻结
class MachineParameters(db.Model):
	__tablename__='machineParameters'
	id=db.Column(db.Integer,primary_key=True)
	eastLongitude=db.Column(db.String)
	northLatitude=db.Column(db.String)
	depth=db.Column(db.String)
	torque=db.Colunm(db.String)
	rotationalSpeed=db.Column(db.String)
	time=db.Column(db.String)
	def __repr__(self):
		return '<MachineParameters %r>'%self.name