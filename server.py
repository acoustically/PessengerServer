from flask import Flask, request, jsonify
from src.routes.user import user
from src.routes.client import client
from src.routes.sms_message import sms_message
from src.rds_connector import Connector

connector = Connector()

app = Flask(__name__)

@app.before_request
def authenticate_token():
  if request.headers.get("Authorization") != "Token acoustically":
    return jsonify(response="error", message="token is invalid")

app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(client, url_prefix="/client")
app.register_blueprint(sms_message, url_prefix="/sms-message")


if __name__ == "__main__":
  app.run(host="0.0.0.0")
