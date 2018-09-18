from flask import request, jsonify
from datetime import datetime, timedelta, date, time
from random import randint
from app import db
from app.api import bp
from app.models import YouthUser, AppWorkloadRecord

@bp.route('/workloads', methods=['GET'])
def get_workload_list():
  workloads = AppWorkloadRecord.query.filter(AppWorkloadRecord.created_at.between(datetime.utcnow() - timedelta(days=30), datetime.utcnow())).order_by(AppWorkloadRecord.created_at.desc()).all()
  result = [i.to_dict() for i in workloads]
  return jsonify({'data': result, 'errCode': 200})

@bp.route('/workloads/<int:id>', methods=['GET'])
def get_workload_by_id(id):
  workload = AppWorkloadRecord.query.get_or_404(id)
  if(workload):
    return jsonify({'data': workload.to_dict(), 'errCode': 200})
  else:
    return jsonify({'errCode': -1, 'errMsg': '数据返回失败', })

@bp.route('/workloads', methods=['POST'])
def insert_workload_record():
  user = YouthUser.query.filter_by(sdut_id=request.form.get('name')).first()
  manager = YouthUser.query.filter_by(sdut_id=request.form.get('manager')).first()
  if(user is None or manager is None):
    return jsonify({'errCode': -1, 'errMsg': '没有此用户'})
  description = request.form.get('description')
  wk_count = request.form.get('wk_count')
  workload = AppWorkloadRecord(name=user.name, department=user.department, description=description, wk_count=wk_count, manager=manager.name)
  try:
    db.session.add(workload)
    db.session.commit()
  except:
    db.session.rollback()
    db.session.flush()
  if(workload.id is None):
    return jsonify({'errCode': -1, 'errMsg': '数据添加失败'})
  workload = AppWorkloadRecord.query.get_or_404(workload.id)
  return jsonify({'errCode': 200, 'errMsg': '数据添加成功'.format(workload.name)})

@bp.route('/workloads/<int:id>', methods=['PUT'])
def upgrade_workload_by_id(id):
  pass

@bp.route('/workloads/<int:id>', methods=['DELETE'])
def del_workload_by_id(id):
  workload = AppWorkloadRecord.query.get_or_404(id)
  db.session.delete(workload)
  db.session.commit()
  return jsonify({'errCode': 200, 'errMsg': '数据删除成功'})