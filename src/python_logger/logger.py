from time import gmtime, strftime
from multipledispatch import dispatch

class Logger():
  def __init__(self, file_path):
    self.file_path = file_path
  
  @dispatch(str)
  def log(self, message):
    self.__write_to_file(message)
    print(message)
    
  @dispatch(str, str)
  def log(self, tag, message):
    log_message = self.__get_time() + "[" + tag + "] : " + message
    self.log(log_message)

  def log_error(self, location, message):
    log_message = self.__get_time() + "[Error] : " + location + " / " + message
    self.log(log_message)

  def request_log(self, method, url):
    log_message = self.__get_time() + method + " / " + url
    self.log(log_message)

  def __get_time(self):
     return strftime("%Y-%m-%d %H:%M:%S - ", gmtime())
  
  def __write_to_file(self, message):
    log_file = open(self.file_path, "a")
    log_file.write(message)
    log_file.close()
    
 
