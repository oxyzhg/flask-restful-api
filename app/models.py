from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app import db

# 用户数据表
class User(db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True, nullable=False)
  email = db.Column(db.String(120), index=True, unique=True, nullable=False)
  password_hash = db.Column(db.String(128))
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return '<User {}>'.format(self.username)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def to_dict(self):
    data = {
      'id': self.id,
      'username': self.username,
      'email': self.email,
      'password': self.password_hash,
      'created_at': self.check_password,
      'updated_at': self.updated_at
    }
    return data

# 青春在线内部用户数据表
class YouthUser(db.Model):
  __tablename__ = "youth_users"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(32), index=True, nullable=False)
  sdut_id = db.Column(db.String(11), index=True, unique=True, nullable=False)
  department = db.Column(db.String(32), nullable=False)
  grade = db.Column(db.String(4), nullable=True)
  phone = db.Column(db.String(11), nullable=False)
  birthday = db.Column(db.String(20), nullable=True)
  role_num = db.Column(db.String(2), default='0') #0默认 1站长 2主任 3管理 4正式 5退站 6试用
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return '<YouthUser {}>'.format(self.sdut_id)

  def to_dict(self):
    data = {
      'id': self.id,
      'name': self.name,
      'sdut_id': self.sdut_id,
      'department': self.department,
      'grade': self.grade,
      'phone': self.phone,
      'birthday': self.birthday,
      'role': self.role_num,
      'dutys': AppSigninDuty.query.filter_by(sdut_id=self.sdut_id).first().to_dict() if(AppSigninDuty.query.filter_by(sdut_id=self.sdut_id).count()) else [],
      'created_at': self.created_at,
      'updated_at': self.updated_at
    }
    return data

# 签到系统值班时间数据表
class AppSigninDuty(db.Model):
  __tablename__ = "app_signin_dutys"

  id = db.Column(db.Integer, primary_key=True)
  sdut_id = db.Column(db.String(11), index=True, unique=True, nullable=False)
  duty_at = db.Column(db.String(32), nullable=False)

  def __repr__(self):
    return '<AppSigninDuty {}>'.format(self.sdut_id)

  def to_dict(self):
    data = {
      # 'id': self.id,
      'sdut_id': self.sdut_id,
      'duty_at': self.duty_at, # 2:1|5:5
    }
    return data

# 签到系统值班记录数据表
class AppSigninRecord(db.Model):
  __tablename__ = "app_signin_records"

  id = db.Column(db.Integer, primary_key=True)
  sdut_id = db.Column(db.String(11), index=True, nullable=False)
  status = db.Column(db.String(2), default='0') #0未签退 1正常值班 2多余值班 3早退 4无效值班
  duration = db.Column(db.String(9), default='0')
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow)
  
  def __repr__(self):
    return '<AppSigninRecord {}>'.format(self.sdut_id)

  def to_dict(self):
    data = {
      'key': self.id,
      'sdut_id': self.sdut_id,
      'status': self.status,
      'duration': self.duration,
      'user': YouthUser.query.filter_by(sdut_id=self.sdut_id).first().to_dict() if(YouthUser.query.filter_by(sdut_id=self.sdut_id).count()) else [],
      'created_at': self.created_at,
      'updated_at': self.updated_at
    }
    return data

# 设备登记表
class AppEquipment(db.Model):
  __tablename__ = "app_equipments"

  id = db.Column(db.Integer, primary_key=True)
  device_name = db.Column(db.String(32), unique=True, nullable=False)
  device_type = db.Column(db.String(32), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow)
  
  def __repr__(self):
    return '<AppEquipment {}>'.format(self.device_name)

  def to_dict(self):
    data = {
      'id': self.id,
      'device_name': self.device_name,
      'device_type': self.device_type
    }
    return data

# 设备使用记录表
class AppDeviceRecord(db.Model):
  __tablename__ = "app_equipment_records"

  id = db.Column(db.Integer, primary_key=True)
  device = db.Column(db.String(32), nullable=False)
  activity = db.Column(db.String(90), nullable=False)
  lend_at = db.Column(db.String(32), nullable=False)
  lend_user = db.Column(db.String(32), nullable=False)
  memo_user = db.Column(db.String(32), nullable=False)
  rememo_user = db.Column(db.String(32), nullable=True)
  return_at = db.Column(db.DateTime, nullable=True)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return '<AppDeviceRecord {}>'.format(self.device)

  def to_dict(self):
    data = {
      'key': self.id,
      'device': self.device,
      'activity': self.activity,
      'lend_at': self.lend_at,
      'lend_user': self.lend_user,
      'memo_user': self.memo_user,
      'rememo_user': self.rememo_user,
      'return_at': self.return_at,
      'created_at': self.created_at,
      'updated_at': self.updated_at
    }
    return data

# 网站日程安排记录表
class AppScheduleRecord(db.Model):
  __tablename__ = "app_schedules"

  id = db.Column(db.Integer, primary_key=True)
  event_name = db.Column(db.String(32), nullable=False)
  event_place = db.Column(db.String(90), nullable=False)
  event_date = db.Column(db.String(32), nullable=False)
  event_status = db.Column(db.String(2), default='0') #0默认 1完成
  sponsor = db.Column(db.String(32), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow)
  
  def __repr__(self):
    return '<AppSchedule {}>'.format(self.event_name)

  def to_dict(self):
    data = {
      'key': self.id,
      'event_name': self.event_name,
      'event_place': self.event_place,
      'event_date': self.event_date,
      'event_status': self.event_status,
      'sponsor': self.sponsor,
      'created_at': self.created_at,
      'updated_at': self.updated_at
    }
    return data

# 网站工作量记录表
class AppWorkloadRecord(db.Model):
  __tablename__ = "app_workloads"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(32), nullable=False)
  department = db.Column(db.String(32), nullable=False)
  description = db.Column(db.String(32), nullable=False)
  wk_count = db.Column(db.String(5), default='0')
  manager = db.Column(db.String(32), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow)
  
  def __repr__(self):
    return '<AppWorkload {}>'.format(self.name)

  def to_dict(self):
    data = {
      'key': self.id,
      'name': self.name,
      'department': self.department,
      'description': self.description,
      'wk_count': self.wk_count,
      'manager': self.manager,
      'created_at': self.created_at,
      'updated_at': self.updated_at
    }
    return data

# 学校行政电话表
class AppPhonebook(db.Model):
  __tablename__ = "app_phonebook"

  id = db.Column(db.Integer, primary_key=True)
  administrative_unit = db.Column(db.String(32), nullable=False)
  office_location = db.Column(db.String(32), nullable=False)
  office_person = db.Column(db.String(32), nullable=True)
  telephone = db.Column(db.String(11), nullable=False)
  notation = db.Column(db.String(32), nullable=True)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow)
  
  def __repr__(self):
    return '<AppWorkload {}>'.format(self.administrative_unit)

  def to_dict(self):
    data = {
      'key': self.id,
      'administrative_unit': self.administrative_unit,
      'office_location': self.office_location,
      'office_person': self.office_person,
      'telephone': self.telephone,
      'notation': self.notation,
      'created_at': self.created_at,
      'updated_at': self.updated_at
    }
    return data