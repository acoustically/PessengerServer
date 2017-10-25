from flask import Blueprint, jsonify, request
from src.rds_connector import Connector
from src.logger import Logger

user = Blueprint('user', __name__)

connector = Connector()
logger = Logger()

def render_err(location, err):
  logger.log_error(location, err)
  return jsonify(response="error", message=err)

@user.route("/")
def all():
  sql = "select * from users"
  result, err = connector.query(sql)
  if err:
    return render_err("/user", err)
  else:
    return jsonify(users=result)

@user.route("/new", methods=["POST"])
def new():
  phone_number = request.form.get("phone_number")
  password = request.form.get("password")
  sql = "insert into users(phone_number, password) values(\"%s\", \"%s\");" % phone_number, password
  result, err = connector.query(sql)
  if err:
    return render_err("/new", err)
  else:
    return jsonify(response="success")
  
@user.route("/<phone_number>")
def show(phone_number):
  sql = "select phone_number from users where phone_number=\"%s\";" % phone_number
  result, err = connector.query(sql)
  if err:
    return render_err("</phone_number>", err)
  else:
    return jsonify(user=result)

