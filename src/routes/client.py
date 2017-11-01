from flask import Blueprint, jsonify, request
from src.rds_connector import Connector

client = Blueprint('client', __name__)

connector = Connector()

@client.route("/new", methods=["POST"])
def new():
  print("TODO")
  #TODO
  
@client.route("/<phone_number>")
def show(phone_number):
  sql = "select name, is_powered from clients where phone_number=\"%s\";" % phone_number
  result, err = connector.query(sql)
  if err:
    return jsonify(clients=list())
  else:
    return jsonify(clients=result)
 
