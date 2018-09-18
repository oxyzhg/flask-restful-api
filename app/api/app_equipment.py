from flask import request, jsonify
from datetime import datetime, timedelta, date, time
from random import randint
from app import db
from app.api import bp
from app.models import YouthUser, AppEquipment, AppDeviceRecord

# 获取所有设备数据表
@bp.route('/equipments', methods=['GET'])
def get_equipment_list():
  equipments = AppEquipment.query.all()
  result = [i.to_dict() for i in equipments]
  return jsonify({'data': result, 'errCode': 200})

# 获取设备信息
@bp.route('/equipments/<int:id>', methods=['GET'])
def get_equipment_by_id(id):
  equipment = AppEquipment.query.get_or_404(id)
  if(equipment):
    return jsonify({'data': equipment.to_dict(), 'errCode': 200})
  else:
    return jsonify({'errCode': -1, 'errMsg': '数据返回失败', })

# 新增设备记录
@bp.route('/equipments', methods=['POST'])
def insert_equipment():
  device_name = request.args.get('device_name')
  device_type = request.args.get('device_type')
  equipment = AppEquipment(device_name=device_name, device_type=device_type)
  try:
    db.session.add(equipment)
    db.session.commit()
  except:
    db.session.rollback()
    db.session.flush()
  if(equipment.id is None):
    return jsonify({'errCode': -1, 'errMsg': '数据添加失败'})
  equipment = AppEquipment.query.get_or_404(equipment.id)
  return jsonify({'errCode': 200, 'errMsg': '设备-{}-添加成功'.format(equipment.device_name)})

# 更新设备信息
@bp.route('/equipments/<int:id>', methods=['PUT'])
def upgrade_equipment(id):
  try:
    equipment = AppEquipment.query.get_or_404(id)
    if(equipment is None):
      return jsonify({'errCode': 1, 'errMsg': '设备不存在'})
    else:
      equipment.device_name = request.args.get('device_name') or equipment.device_name
      equipment.device_type = request.args.get('device_type') or equipment.device_type
      equipment.updated_at = datetime.utcnow()
      db.session.add(equipment)
      db.session.commit()
  except:
    db.session.rollback()
    db.session.flush()
  equipment = AppEquipment.query.get_or_404(id)
  return jsonify({'errCode': 200, 'data': equipment.to_dict()})

# 删除设备记录
@bp.route('/equipments/<int:id>', methods=['DELETE'])
def del_equipment_by_id(id):
  equipment = AppEquipment.query.get_or_404(id)
  db.session.delete(equipment)
  db.session.commit()
  return jsonify({'errCode': 200, 'errMsg': '数据删除成功'})

# 获取30天内所有设备借用记录数据表
@bp.route('/devices', methods=['GET'])
def get_device_list():
  records = AppDeviceRecord.query.filter(AppDeviceRecord.created_at.between(datetime.utcnow() - timedelta(days=30), datetime.utcnow())).order_by(AppDeviceRecord.created_at.desc()).all()
  result = [i.to_dict() for i in records]
  return jsonify({'data': result, 'errCode': 200})

# 新增设备借用记录
@bp.route('/devices', methods=['POST'])
def insert_device_record():
  device_status = AppDeviceRecord.query.filter_by(device=request.form.get('device')).order_by(AppDeviceRecord.created_at.desc()).first()
  if(device_status and device_status.return_at is None):
    return jsonify({'errCode': -1, 'errMsg': '设备在借用状态'})
  device = request.form.get('device')
  activity = request.form.get('activity')
  lend_at = request.form.get('lend_at')
  lend_user = request.form.get('lend_user')
  memo_user = YouthUser.query.filter_by(sdut_id=request.form.get('memo_user')).first()
  if(memo_user is None):
    return jsonify({'errCode': -1, 'errMsg': '备忘人不存在'})
  record = AppDeviceRecord(device=device, activity=activity, lend_at=lend_at, lend_user=lend_user, memo_user=memo_user.name)
  try:
    db.session.add(record)
    db.session.commit()
  except:
    db.session.rollback()
    db.session.flush()
  if(record.id is None):
    return jsonify({'errCode': -1, 'errMsg': '数据添加失败'})
  record = AppDeviceRecord.query.get_or_404(record.id)
  return jsonify({'errCode': 200, 'errMsg': '设备-{}-添加成功'.format(record.device)})

# 更新设备借用记录
@bp.route('/devices/<int:id>', methods=['PUT'])
def upgrade_device_record(id):
  try:
    record = AppDeviceRecord.query.get_or_404(id)
    rememo_user = YouthUser.query.filter_by(sdut_id=request.form.get('rememo_user')).first()
    if(record is None):
      return jsonify({'errCode': 1, 'errMsg': '记录不存在'})
    elif(record.return_at is not None):
      return jsonify({'errCode': 1, 'errMsg': '设备已归还'})
    elif(rememo_user is None):
      return jsonify({'errCode': -1, 'errMsg': '备忘人不存在'})
    else:
      record.device = record.device
      record.activity = record.activity
      record.lend_at = record.lend_at
      record.lend_user = record.lend_user
      record.memo_user = record.memo_user
      record.rememo_user = rememo_user.name
      record.return_at = datetime.utcnow()
      record.updated_at = datetime.utcnow()
      db.session.add(record)
      db.session.commit()
  except:
    db.session.rollback()
    db.session.flush()
  record = AppDeviceRecord.query.get_or_404(id)
  return jsonify({'errCode': 200, 'data': record.to_dict()})

# 删除设备借用记录
@bp.route('/devices/<int:id>', methods=['DELETE'])
def del_device_record_by_id(id):
  record = AppDeviceRecord.query.get_or_404(id)
  user = YouthUser.query.filter_by(sdut_id=request.args.get('user')).first()
  if(user is None):
    return jsonify({'errCode': -1, 'errMsg': '没有管理权限'})
  db.session.delete(record)
  db.session.commit()
  return jsonify({'errCode': 200, 'errMsg': '数据删除成功'})