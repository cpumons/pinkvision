from raspsoft import *

class Controller():
    """
    This class represents the controller that is used to control the car.
    """
    def __init__(self):
        self.car = Car()
        self.actions = [Forward(65,1),Backward(60,1),TurnRight(50),TurnLeft(130)]
        self.state = "idle"
        self.direction = "none"
        self.debug = False

    def add_forward(self):
        if (self.debug):
            print("add forward..")
        self.state = "running"
        self.car.add_state(self.actions[0])
    
    def rm_forward(self):
        if (self.debug):
            print("remove forward..")
        self.state = "idle"
        self.car.remove_state(self.actions[0])

    def add_right(self):
        if (self.debug):
            print("add right..")
        self.direction = "right"
        self.car.add_state(self.actions[2])
    
    def rm_right(self):
        if (self.debug):
            print("remove right")
        self.direction = "none"
        self.car.remove_state(self.actions[2])
    
    def add_left(self):
        if (self.debug):
            print("add left..")
        self.direction = "left"
        self.car.add_state(self.actions[3])
    
    def rm_left(self):
        if (self.debug):
            print("remove left")
        self.direction = "none"
        self.car.remove_state(self.actions[3])