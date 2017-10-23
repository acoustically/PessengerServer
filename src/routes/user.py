from flask import Blueprint, jsonify, request
from src.rds_connector import Connector

user = Blueprint('user', __name__)

connector = Connector()

@user.route("/")
def all():
  print(1)
  sql = "select * from users"
  print(2)
  result, err = connector.query(sql)
  print(3)
  if err:
    return jsonify(response="error", message="db error")
  else:
    return jsonify(users=result)

@user.route("/new", methods=["POST"])
def new():
  phone_number = request.form.get("phone_number")
  password = request.form.get("password")
  sql = "insert into users(phone_number, password) values(\"%s\", \"%s\");" % phone_number, password
  result, err = connector.query(sql)
  if err:
    return jsonify(response="error", message=err)
  else:
    return jsonify(response="success")
  
@user.route("/<phone_number>")
def show(phone_number):
  sql = "select phone_number from users where phone_number=\"%s\";" % phone_number
  result, err = connector.query(sql)
  if err:
    return jsonify(response="error", message=err)
  else:
    return jsonify(user=result)
 
