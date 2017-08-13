import threading
import json

_buffer_size = 1024

class SocketReadThread(threading.Thread):

  def __init__(self, socket):
    threading.Thread.__init__(self)
    self._socket = socket

  def run(self):
    data_bytes = self.__recv_data()
    data_unicode = self.__data_bytes_to_unicode(data_bytes)
    #print(data_unicode)
    data_json = json.loads(data_unicode)
    print(data_json["client"])
    
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
    
