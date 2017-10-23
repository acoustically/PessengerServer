import src.python_mysql_connector.mysql_connector as mysql

class Connector(mysql.Connector):
  def __init__(self):
    mysql.Connector.__init__(self, host="pessenger.crsnodt9hkzk.ap-northeast-2.rds.amazonaws.com",
                             user="acoustically",
                             password="PEsung1031!",
                             db="Pessenger")

