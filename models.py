from . import db
#RFID卡：卡号/用户编号/发卡时间/是否冻结
class RfidCard(db.Model):
	__tablename__='rfidcard'
	id=db.Column(db.Integer,primary_key=True)
	car_id=db.Column(db.String(64),unique=True)
	user_id=db.Column(db.String(64),unique=True)
	card_time=db.Column(db.String(64))
	freeze=db.Column(db.String(64))
	def __repr__(self):
		return '<RfidCard %r>'%self.name