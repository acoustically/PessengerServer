import src.python_logger.logger as python_logger
import os, inspect

class Logger(python_logger.Logger):
  def __init__(self):
    self.log_file_path = os.path.dirname(os.path.abspath(inspect.stack()[0][1])) + "/../log.txt"
    python_logger.Logger.__init__(self, self.log_file_path)
