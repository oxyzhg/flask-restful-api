from flask import request, jsonify
from datetime import datetime, timedelta, date, time
from random import randint
from app import db
from app.api import bp
from app.models import YouthUser, AppScheduleRecord

@bp.route('/schedules', methods=['GET'])
def get_schedule_list():
  events = AppScheduleRecord.query.filter(AppScheduleRecord.created_at.between(datetime.utcnow() - timedelta(days=30), datetime.utcnow())).order_by(AppScheduleRecord.created_at.desc()).all()
  result = [i.to_dict() for i in events]
  return jsonify({'data': result, 'errCode': 200})
  
@bp.route('/schedules/<int:id>', methods=['GET'])
def get_schedule_by_id(id):
  event = AppScheduleRecord.query.get_or_404(id)
  if(event):
    return jsonify({'data': event.to_dict(), 'errCode': 200})
  else:
    return jsonify({'errCode': -1, 'errMsg': '数据返回失败', })

@bp.route('/schedules', methods=['POST'])
def insert_schedule_record():
  sponsor = YouthUser.query.filter_by(sdut_id=request.form.get('sponsor')).first()
  if(sponsor is None):
    return jsonify({'errCode': -1, 'errMsg': '没有此用户'})
  event_name = request.form.get('event_name')
  event_place = request.form.get('event_place')
  event_date = request.form.get('event_date')
  event = AppScheduleRecord(event_name=event_name, event_place=event_place, event_date=event_date, sponsor=sponsor.name)
  try:
    db.session.add(event)
    db.session.commit()
  except:
    db.session.rollback()
    db.session.flush()
  if(event.id is None):
    return jsonify({'errCode': -1, 'errMsg': '数据添加失败'})
  event = AppScheduleRecord.query.get_or_404(event.id)
  return jsonify({'errCode': 200, 'errMsg': '添加成功'.format(event.event_name)})


@bp.route('/schedules/<int:id>', methods=['PUT'])
def upgrade_schedule_by_id(id):
  user = YouthUser.query.filter_by(sdut_id=request.form.get('user')).first()
  if(user is None):
    return jsonify({'errCode': -1, 'errMsg': '没有此用户'})
  try:
    event = AppScheduleRecord.query.get_or_404(id)
    if(event is None):
      return jsonify({'errCode': 1, 'errMsg': '设备不存在'})
    else:
      event.event_name = request.form.get('event_name') or event.event_name
      event.event_place = request.form.get('event_place') or event.event_place
      event.event_date = request.form.get('event_date') or event.event_date
      event.sponsor = request.form.get('sponsor') or event.sponsor
      event.event_status = '1'
      event.updated_at = datetime.utcnow()
      db.session.add(event)
      db.session.commit()
  except:
    db.session.rollback()
    db.session.flush()
  event = AppScheduleRecord.query.get_or_404(id)
  return jsonify({'errCode': 200, 'data': event.to_dict()})

@bp.route('/schedules/<int:id>', methods=['DELETE'])
def del_schedule_by_id(id):
  event = AppScheduleRecord.query.get_or_404(id)
  db.session.delete(event)
  db.session.commit()
  return jsonify({'errCode': 200, 'errMsg': '数据删除成功'})