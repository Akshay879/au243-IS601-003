import math
class Triangle():
    def __init__(self,base,height):
        self.base = base
        self.height = height

    def hypotenuse(self):
        return math.sqrt(self.base**2 + self.height**2)
    
    def area(self):
        return 1/2 * self.base * self.height
    
    def __str__(self):
        print(f"Triangle: base={self.base}, height={self.height}")

    
