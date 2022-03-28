import RPi.GPIO as GPIO
import time
import thread_soft as threads

GPIO.setwarnings(False)
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

    def __init__(self,speed):
        self.pwm_freq = 100
        self.speed = speed

    def run(self):
        self.thread = threads.thread_with_trace(target = self.thread_start)
        self.thread.start()

    def thread_start(self):
        pwm_cc.ChangeFrequency(self.pwm_freq)
        GPIO.output(13,1)
        GPIO.output(15,0)
        pwm_cc.start(self.speed)

    def stop(self):
        pwm_cc.stop()
        GPIO.output(13, 1)
        GPIO.output(15, 0)
        self.thread.kill()
        

class Backward(State):

    def __init__(self,speed):
        self.pwm_freq = 100
        self.speed = speed

    def run(self):
        self.thread = threads.thread_with_trace(target = self.thread_start)
        self.thread.start()
    
    def thread_start(self):
        pwm_cc.ChangeFrequency(self.pwm_freq)
        GPIO.output(13,0)
        GPIO.output(15,1)
        pwm_cc.start(self.speed)

    def stop(self):
        pwm_cc.stop()
        GPIO.output(13, 0)
        GPIO.output(15 ,1)
        self.thread.kill()

class TurnRight(State):
    
    def __init__(self,target_angle):
        self.target_angle = target_angle

    def run(self):
        self.thread = threads.thread_with_trace(target = self.thread_start)
        self.thread.start()

    def thread_start(self):
        if(self.target_angle > 90 or self.target_angle < 30):
            raise Exception("Target angle must be between 30 and 90 for TurnRight")
        return_angle = 90
        while(return_angle > self.target_angle):
            pwm_servo.start(angle_to_percent(return_angle))
            time.sleep(0.02)
            return_angle -= 1

    def stop(self):
        self.thread.kill()
        pwm_servo.ChangeDutyCycle(angle_to_percent(90))
        time.sleep(0.01)

class TurnLeft(State):

    def __init__(self,target_angle):
        self.target_angle = target_angle

    def run(self):
        self.thread = threads.thread_with_trace(target = self.thread_start)
        self.thread.start()

    def thread_start(self):
        if(self.target_angle <= 90 or self.target_angle >= 150):
            raise Exception("Target angle must be between 90 and 150 for TurnLeft")
        return_angle = 90
        while(return_angle < self.target_angle):
            pwm_servo.start(angle_to_percent(return_angle))
            time.sleep(0.02)
            return_angle += 1

    def stop(self):
        self.thread.kill()
        pwm_servo.ChangeDutyCycle(angle_to_percent(90))
        time.sleep(0.01)
    
if __name__ == "__main__":
    car = Car()
    backward = Backward(60)
    forward = Forward(60)
    turnRight = TurnRight(30)
    turnLeft = TurnLeft(150)
    car.add_state(forward)
    time.sleep(2)
    car.add_state(turnRight)
    time.sleep(0.5)
    car.remove_state(forward)
    time.sleep(1)
    car.remove_state(turnRight)
