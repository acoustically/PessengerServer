import threading
import json

_buffer_size = 1024

class SocketReadThread(threading.Thread):

  def __init__(self, socket, socket_list):
    threading.Thread.__init__(self)
    self._socket = socket
    self._socket_list = socket_list

  def run(self):
    data_bytes = self.__recv_data()
    data_unicode = self.__data_bytes_to_unicode(data_bytes)
    #print(data_unicode)
    data_json = json.loads(data_unicode)

    if(data_json["client"] == "windows"):
      self._socket_list.append(self._socket)
      print(len(self._socket_list))
    elif(data_json["client"] == "android"):
      if(data_json["action"] == "receiveSmsMessage"):
        self.__send_data(self._socket_list, data_unicode)
        print(len(self._socket_list))
      elif(data_json["action"] == "userValidation"):
        self._socket.send(bytes(data_unicode, "utf-8"))
        self._socket.close()
        print("test user validation")
    
  def __send_data(self, socket_list, data):
    for socket in socket_list:
      try:
        socket.send(bytes(data, "utf-8"))
        print("send data")
      except:
        print("send error")
        socket.close()
        socket_list.remove(socket)

  def __recv_data(self):
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
