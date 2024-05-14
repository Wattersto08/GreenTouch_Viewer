

class Object:
    def __init__(self, name, coords, Type):
        self.name = name
        self.coords = coords
        self.Type = Type
        
    def __str__(self):
        return f"{self.name} ({self.Type})"
    
    def dumpdata(self):
        print(self.name)
        print(self.coords)
        print(self.Type)