from flask import Blueprint, jsonify, request
from src.rds_connector import Connector

user = Blueprint('user', __name__)

connector = Connector()


@user.route("/new", methods=["POST"])
def new():
  json = request.get_json()
  phone_number = json["phone_number"]
  password = json["password"]
  print(phone_number)
  print(password)
  sql = "insert into users(phone_number, password) values(\"%s\", \"%s\");" % (phone_number, password)
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
    return jsonify(response="fail", error=err["message"])
  else:
    return jsonify(response="success")

