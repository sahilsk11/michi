import math

cartype_f1 = "f1"

class Car:
  def __init__(self, cartype=cartype_f1):
    if cartype == cartype_f1:
      self.a = 136.3384438
      self.b = 65.165567

  def speed(self, t):
    return self.a + self.b * math.log(t)
