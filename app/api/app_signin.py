from flask import request, jsonify
from datetime import datetime, timedelta, date, time
from random import randint
from app import db
from app.api import bp
from app.models import AppSigninDuty, AppSigninRecord, YouthUser

# 获取当日签到记录数据表
@bp.route('/signin', methods=['GET'])
def get_signin_list():
  records = AppSigninRecord.query.filter(AppSigninRecord.created_at.between(datetime.utcnow().date(), datetime.utcnow().date() + timedelta(days=1))).order_by(AppSigninRecord.created_at.desc()).all()
  result = [i.to_dict() for i in records]
  return jsonify({'data': result, 'errCode': '数据返回成功'})

# 签到或签退操作
@bp.route('/signin', methods=['POST'])
def upgrade_signin_record():
  sdut_id = request.form.get('sdut_id')
  user = YouthUser.query.filter_by(sdut_id=sdut_id).first()
  record = AppSigninRecord.query.filter(AppSigninRecord.created_at.between(datetime.utcnow().date(), datetime.utcnow().date() + timedelta(days=1))).filter_by(sdut_id=sdut_id).order_by(AppSigninRecord.created_at.desc()).first()
  if(user):
    #若有记录，则为更新操作；若无记录，则为增加操作
    if(record and record.status == '0'):
      user = user.to_dict()
      if(user['role'] == '5'):
        record.status = 4 #若已退站，标注为无效值班
      else:
        timer = 70        #单次值班时长
        is_today = False  #值班判断条件
        duty_area = '0'   #值班区间
        duration = (datetime.utcnow() - record.created_at).seconds #值班时长
        dutys = user['dutys']['duty_at'].split('|')             #数据表中值班区间
        current_now = datetime.utcnow()                            #当前时间
        current_day = datetime.strptime(current_now.date().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') #当天凌晨时间
        
        #判断当天是否有值班任务，有则更新值班判断条件和值班区间
        for duty in dutys:
          if(duty[0:1] == str(date.isoweekday(datetime.utcnow()))):
            is_today = True
            duty_area = duty[2:]
            break

        #若有值班任务，则判断值班情况；若无值班任务，则为多于值班
        if(is_today):
          #根据值班区间，更新时间段内的起始时间点
          if(duty_area == '1'):
            start_at = current_day + timedelta(hours=8, minutes=0)
            end_at = current_day + timedelta(hours=9, minutes=50)
          elif(duty_area == '2'):
            start_at = current_day + timedelta(hours=10, minutes=10)
            end_at = current_day + timedelta(hours=12, minutes=0)
          elif(duty_area == '3'):
            start_at = current_day + timedelta(hours=14, minutes=0)
            end_at = current_day + timedelta(hours=15, minutes=50)
          elif(duty_area == '4'):
            start_at = current_day + timedelta(hours=16, minutes=0)
            end_at = current_day + timedelta(hours=17, minutes=50)
          elif(duty_area == '5'):
            start_at = current_day + timedelta(hours=19, minutes=0)
            end_at = current_day + timedelta(hours=20, minutes=50)
            
          if(record.created_at < start_at and current_now < end_at and current_now > start_at):
            # 签到时间比规定时间早，签退时间比规定时间早
            duration = (current_now - start_at).seconds
          elif(record.created_at < start_at and current_now > end_at):
            # 签到时间比规定时间早，签退时间比规定时间晚
            duration = (end_at - start_at).seconds
          elif(record.created_at > start_at and current_now > end_at and record.created_at < end_at):
            # 到时间比规定时间晚，签退时间比规定时间晚
            duration = (end_at - record.created_at).seconds
          elif(record.created_at > start_at and current_now < end_at):
            # 签到时间比规定时间晚，签退时间比规定时间早
            duration = (current_now - record.created_at).seconds
          
          if(record.created_at > end_at or current_now < start_at):
            record.status = '2' if(duration >= timer) else '4'
          else:
            record.status = '1' if(duration >= timer) else '3'
        else:
          record.status = '2' if(duration < timer) else '4'
      # 保存更改
      record.updated_at = datetime.utcnow()
      db.session.add(record)
      db.session.commit()
    else:
      #没有数据新增
      record = AppSigninRecord(sdut_id=sdut_id)
      try:
        db.session.add(record)
        db.session.commit()
      except:
        db.session.rollback()
        db.session.flush()
      if(record.id is None):
        return jsonify({'errCode': -1, 'errMsg': '数据添加失败'})
    record = AppSigninRecord.query.filter(AppSigninRecord.created_at.between(datetime.utcnow().date(), datetime.utcnow().date() + timedelta(days=1))).filter_by(sdut_id=sdut_id).order_by(AppSigninRecord.created_at.desc()).first()
    # 操作结束后，返回此次更新结果
    return jsonify({'data': record.to_dict(), 'errCode': 200 })
  else:
    return jsonify({'errCode': -1, 'errMsg': '用户不存在'})


# 删除签到记录
@bp.route('/signin/<int:id>', methods=['DELETE'])
def del_signin_record_by_id(id):
  record = AppSigninRecord.query.get_or_404(id)
  db.session.delete(record)
  db.session.commit()
  return jsonify({'errCode': 200, 'errMsg': '数据删除成功'})