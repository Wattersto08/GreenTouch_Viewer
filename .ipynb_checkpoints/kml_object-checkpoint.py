import random 

color_options = ['blue',  'darkgreen', 'darkred', 'green', 'lightblue', 'lightgray', 'lightgreen', 'orange', 'pink','purple', 'red', 'white']

class Object:
    global color_options
    
    def __init__(self, name, coords, Type):
        self.name = name
        self.coords = coords
        self.Type = Type
        self.color = color_options[random.randint(0,len(color_options)-1)]
        
    def __str__(self):
        return f"{self.name} ({self.Type})"
    
    def dumpdata(self):
        print(self.name)
        print(self.Type)
        print(self.color)
        print(self.coords)
        
        