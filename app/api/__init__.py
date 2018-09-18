from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import users, app_signin, app_equipment, app_schedule, app_workload, app_phonebook
