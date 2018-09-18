from flask import request, jsonify
from datetime import datetime, timedelta, date, time
from random import randint
from app import db
from app.api import bp
from app.models import YouthUser, AppPhonebook

@bp.route('/phones', methods=['GET'])
def get_phone_list():
  phones = AppPhonebook.query.all()
  result = [i.to_dict() for i in phones]
  return jsonify({'data': result, 'errCode': 200})

@bp.route('/phones/<int:id>', methods=['GET'])
def get_phone_by_id(id):
  phone = AppPhonebook.query.get_or_404(id)
  if(phone is None):
    return jsonify({'errCode': -1, 'errMsg': '查不到相关数据'})
  else:
    return jsonify({'data': phone.to_dict(), 'errCode': 200})

@bp.route('/phones', methods=['POST'])
def insert_phone_record():
  administrative_unit = request.args.get('administrative_unit')
  office_location = request.args.get('office_location')
  office_person = request.args.get('office_person')
  telephone = request.args.get('telephone')
  notation = request.args.get('notation')
  if(administrative_unit is None or office_location is None or telephone is None):
    return jsonify({'errCode': -1, 'errMsg': '数据不完整'})
  phone = AppPhonebook(administrative_unit=administrative_unit, office_location=office_location, office_person=office_person, telephone=telephone, notation=notation)
  try:
    db.session.add(phone)
    db.session.commit()
  except:
    db.session.rollback()
    db.session.flush()
  if(phone.id is None):
    return jsonify({'errCode': -1, 'errMsg': '数据添加失败'})
  phone = AppPhonebook.query.get_or_404(phone.id)
  return jsonify({'errCode': 200, 'errMsg': '数据添加成功'})

@bp.route('/phones/<int:id>', methods=['PUT'])
def upgrade_phone_by_id(id):
  pass

@bp.route('/phones/<int:id>', methods=['DELETE'])
def del_phone_by_id(id):
  phone = AppPhonebook.query.get_or_404(id)
  db.session.delete(phone)
  db.session.commit()
  return jsonify({'errCode': 200, 'errMsg': '数据删除成功'})