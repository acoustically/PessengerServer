from flask import Blueprint, jsonify, request
from src.rds_connector import Connector

sms_message = Blueprint('sms_message', __name__)

connector = Connector()

@sms_message.route("/new", methods=["POST"])
def new():
  json = request.get_json()
  phone_number = json["phone_number"]
  from_ = json["from_"]
  body = json["body"]
  
  sql = 'select id, is_connected from clients where phone_number="%s";' % phone_number

  clients, err = connector.query(sql)
  if err:
    return ""
  else:
    for client in clients:
      if client["is_connected"] == 1:
        sql = 'select count(*) from sms_messages where phone_number="%s" and client_id=%s;' % (phone_number, client["id"])
        result, err = connector.query(sql)
        if result[0]["count(*)"] > 0:
          sql = 'delete from sms_messages where phone_number="%s" and client_id=%s;' % (phone_number, client["id"])
          connector.query(sql)
        sql = 'insert into sms_messages(client_id, phone_number, from_, body) values(%s, "%s", "%s", "%s");' % (client["id"], phone_number, from_, body)
        connector.query(sql)
    return ""

@sms_message.route("/<phone_number>/<client_id>")
def show(phone_number, client_id):
  sql = 'select from_, body from sms_messages where phone_number="%s" and client_id=%s;' % (phone_number, client_id)
  result, err = connector.query(sql)
  if err:
    return jsonify(response="fail", error=err)
  else:
    sql = 'delete from sms_messages where phone_number="%s" and client_id=%s;' % (phone_number, client_id)
    connector.query(sql)
    return jsonify(sms_message=result)
 
