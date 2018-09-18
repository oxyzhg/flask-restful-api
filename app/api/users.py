from flask import request, jsonify
from datetime import datetime
from app import db
from app.api import bp
from app.models import YouthUser

@bp.route('/test', methods=['GET'])
def test():
  return jsonify({ 'data': 132 })

# 获取用户列表
@bp.route('/youthusers', methods=['GET'])
def get_youthuser_list():
  users = YouthUser.query.all()
  result = [i.to_dict() for i in users]
  return jsonify({'data': result, 'errCode': 200})

# 获取用户信息
@bp.route('/youthuser/<int:id>', methods=['GET'])
def get_youthuser_by_id(id):
  user = YouthUser.query.get_or_404(id)
  if(user):
    return jsonify({'data': user.to_dict(), 'errCode': 200})
  else:
    return jsonify({'errCode': -1, 'errMsg': '数据返回失败', })

# 新增用户
@bp.route('/youthuser', methods=['POST'])
def insert_youthuser():
  name = request.args.get('name')
  sdut_id = request.args.get('sdut_id')
  department = request.args.get('department')
  grade = request.args.get('grade')
  phone = request.args.get('phone')
  birthday = request.args.get('birthday')
  role_num = request.args.get('role')
  user = YouthUser(name=name, sdut_id=sdut_id, department=department, grade=grade, phone=phone, birthday=birthday, role_num=role_num)
  try:
    db.session.add(user)
    db.session.commit()
  except:
    db.session.rollback()
    db.session.flush()
  if(user.id is None):
    return jsonify({'errCode': -1, 'errMsg': '数据添加失败'})
  result = YouthUser.query.get_or_404(user.id)
  return jsonify({'errCode': 200, 'errMsg': '用户-{}-添加成功'.format(user.name)})

# 修改用户信息
@bp.route('/youthuser/<int:id>', methods=['PUT'])
def upgrade_youthuser_by_id(id):
  try:
    user = YouthUser.query.get_or_404(id)
    if(user is None):
      return jsonify({'errCode': 1, 'errMsg': '用户不存在'})
    else:
      user.name = request.args.get('name')
      user.sdut_id = request.args.get('sdut_id')
      user.department = request.args.get('department')
      user.grade = request.args.get('grade')
      user.phone = request.args.get('phone')
      user.birthday = request.args.get('birthday')
      user.role_num = request.args.get('role')
      user.updated_at = datetime.utcnow()
      db.session.add(user)
      db.session.commit()
  except:
    db.session.rollback()
    db.session.flush()
  user = YouthUser.query.get_or_404(id)
  return jsonify({'errCode': -1, 'data': user.to_dict()})

# 删除用户
@bp.route('/youthuser/<int:id>', methods=['DELETE'])
def del_youthuser_by_id(id):
  user = YouthUser.query.get_or_404(id)
  db.session.delete(user)
  db.session.commit()
  return jsonify({'errCode': 200, 'errMsg': '数据删除成功'})