import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
pwm_cc = GPIO.PWM(32, 100)
pwm_servo = GPIO.PWM(12, 50)

"""
    Compute PWM percent of a given angle.
    Used to rotate the servo.
"""
def angle_to_percent (angle) :
    if angle > 180 or angle < 0 :
        return False

    start = 4
    end = 12.5
    ratio = (end - start)/180 #Calcul ratio from angle to percent

    angle_as_percent = angle * ratio

    return start + angle_as_percent

"""
    Implements car which is the context of the state design pattern used.
    Contains a list of states. If the list contains a state, it means that the state is currently running.
"""
class Car():

    def __init__(self):
        self.states = []

    def add_state(self, state):
        self.states.append(state)
        state.run()

    def remove_state(self, state):
        state.stop()
        self.states.remove(state)
"""
    Abstract class that implements state which can be started or stopped.
"""
class State():

    def __init__(self):
        pass

    def run(self):
        pass

    def stop(self):
        pass

class Forward(State):

    def __init__(self):
        self.pwm_freq = 100
        self.speed = 70

    def run(self):
        pwm_cc.ChangeFrequency(self.pwm_freq)
        GPIO.output(13,1)
        GPIO.output(15,0)
        pwm_cc.start(self.speed)

    def stop(self):
        pwm_cc.stop()
        GPIO.output(13, 0)
        GPIO.output(15, 0)
        

class Backward(State):

    def __init__(self):
        self.pwm_freq = 100
        self.speed = 40

    def run(self):
        pwm_cc.ChangeFrequency(self.pwm_freq)
        GPIO.output(13,0)
        GPIO.output(15,1)
        pwm_cc.start(self.speed)

    def stop(self):
        pwm_cc.stop()
        GPIO.output(13, 0)
        GPIO.output(15 ,1)

class TurnRight(State):
    
    def __init__(self):
        pass

    def run(self):
        pwm_servo.start(angle_to_percent(30))

    def stop(self):
        pwm_servo.ChangeDutyCycle(angle_to_percent(90))
        time.sleep(0.01)

class TurnLeft(State):

    def __init__(self):
        pass

    def run(self):
        pwm_servo.start(angle_to_percent(150))

    def stop(self):
        pwm_servo.ChangeDutyCycle(angle_to_percent(90))
        time.sleep(0.01)
    
if __name__ == "__main__":
    car = Car()
    backward = Backward()
    forward = Forward()
    turnRight = TurnRight()
    turnLeft = TurnLeft()
    car.add_state(forward)
    time.sleep(1)
    car.remove_state(forward)
    car.add_state(backward)
    time.sleep(1)
    car.remove_state(backward)
    car.add_state(turnRight)
    car.add_state(forward)
    time.sleep(1)
    car.remove_state(turnRight)
    car.add_state(turnLeft)
    time.sleep(1)
    car.remove_state(turnLeft)
    car.remove_state(forward)
    pwm_servo.stop()
    pwm_cc.stop()
    GPIO.cleanup()

