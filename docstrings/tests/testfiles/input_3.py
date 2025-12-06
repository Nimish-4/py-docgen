import math


class xyz:
  def __init__(self, a, b):
        
        self.a = a
        self.b = b
    
  def calculate_log(self):
        """Return sum of logarithms of `a` and `b`"""

        def log(x):
            return math.log(x)

        return log(self.a) + log(self.b)