import threading
import json
import pymysql

_buffer_size = 1024

class SocketReadWriteThread(threading.Thread):

  def __init__(self, socket, socket_list):
    threading.Thread.__init__(self)
    self._socket = socket
    self._socket_list = socket_list

  def run(self):
    data_bytes = self.__receive()
    data_unicode = self.__data_bytes_to_unicode(data_bytes)
    #print(data_unicode)
    data_json = json.loads(data_unicode)

    if(data_json["client"] == "windows"):
      self._socket_list.append(self._socket)
      print(len(self._socket_list))
    elif(data_json["client"] == "android"):
      if(data_json["action"] == "receiveSmsMessage"):
        self.__send_to_all(self._socket_list, data_unicode)
        print(len(self._socket_list))
      elif(data_json["action"] == "logIn"):
        print("try to log in : " + data_json["phoneNumber"])
        account = self.__query_account(data_json["phoneNumber"])
        if(any(account)): # if account exist in database
          self.__send(b'1')
        else:
          self.__send(b'0')
      elif(data_json["action"] == "signUp"):
        print("try to sign up : " + data_json["phoneNumber"] + " " + data_json["password"])
        account = self.__insert_account(data_json["phoneNumber"], data_json["password"])
        if(any(account)):
          self.__send(b'1')
        else:
          self.__send(b'0')
        

  def __send(self, data):
    self._socket.send(data)
    self._socket.close();  
  
  def __send_to_all(self, socket_list, data):
    for socket in socket_list:
      try:
        print("send data")
        socket.send(bytes(data, "utf8"))
      except:
        print("send error")
        socket.close()
        socket_list.remove(socket)

  def __receive(self):
    data = b''

    while(1):
      data_piece = self._socket.recv(_buffer_size)
      data += data_piece
      if(len(data) < _buffer_size):
        break;

    return data

  def __data_bytes_to_unicode(self, data_bytes):
    data_unicode = data_bytes.decode('utf-8', errors='replace')
    json_begin = data_unicode.find("{")
    json_end = data_unicode.find("}") + 1
    data_unicode = data_unicode[json_begin:json_end]
    return data_unicode

  def __connect_db(self):
    connection = pymysql.connect(host='pessenger.crsnodt9hkzk.ap-northeast-2.rds.amazonaws.com', 
                                 user='acoustically', 
                                 password='PEsung1031!',
                                 db='Pessenger',
                                 charset='utf8')
    return connection

  def __query_account(self, phone_number):
    connection = self.__connect_db()
    cursor = connection.cursor()
    sql = "select phone_number from users where phone_number=\'" + phone_number + "\';"
    print("sql : " + sql)
    cursor.execute(sql)
    recode = cursor.fetchall()
    print("result : ")
    print(recode)
    connection.close()
    return recode

  def __insert_account(self, phone_number, password):
    connection = self.__connect_db()
    cursor = connection.cursor()
    sql = "insert into users(phone_number, password) values(\'" + phone_number+ "\',\'" + password + "\');"
    print("sql : " + sql)
    print(cursor.execute(sql))
    connection.commit()
    connection.close()
    return self.__query_account(phone_number)
    
