from flask import Flask, request, jsonify
from src.routes.user import user
import logging
from src.logger import Logger
from src.rds_connector import Connector

connector = Connector()

logger = Logger()

app = Flask(__name__)
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True

@app.before_request
def before_request():
  logger.request_log(request.method, request.url)

@app.before_request
def authenticate_token():
  if request.headers.get("token") != "acoustically":
    return jsonify(response="error", message="token is invalid")

app.register_blueprint(user, url_prefix="/user")

if __name__ == "__main__":
  app.run()
