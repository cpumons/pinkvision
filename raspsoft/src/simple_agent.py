from lane_detection import *
from controller import *
import cv2

class Agent():
    """
    Simple reflex agent which aims to follow the lane.
    """
    def __init__(self):
        self.controller = Controller()
        self.camera = cv2.VideoCapture(0, cv2.CAP_V4L)
        self.iterations_count = 0
        self.debug = False
     
    def run(self):
        """
        Loop that runs the agent.
        The loop time is 0.02 sec without debugging and 0.07 with debugging
        """
        while(True):
            self.iterations_count += 1
            road_info = self.sensors_sampling()
            self.decision_making(road_info)

    def sensors_sampling(self):
        """
        Take a picture and returns the lanes positions.
        """
        _, frame = self.camera.read()
        road_info =  get_lane_lines(frame)
        output_name = "picture"+str(self.iterations_count)+".png"
        if (self.debug):
            print("new iteration : " + str(self.iterations_count))
            print(road_info.left_lane)
            print(road_info.right_lane)
            black_lines = display_lines(frame, [road_info.left_lane, road_info.right_lane])
            frame_lanes = cv2.addWeighted(frame, 0.9, black_lines, 1, 1)
            cv2.imwrite('./photos/'+output_name, frame_lanes)

        return road_info

    def decision_making(self, road_info):
        """
        Decides what action to take according to lanes position.
        """
        isLeft = True
        isRight = True
        if (len(road_info.left_lane) == 0):
            isLeft = False
        if (len(road_info.right_lane) == 0):
            isRight = False

        if (self.controller.state == "idle"):
            if (isLeft and isRight):
                self.controller.add_forward()

        elif (self.controller.state == "running"):
            #state == "running"
            if ((not isRight) and isLeft and self.controller.direction != "right"):
                self.controller.add_right()
            if ((not isLeft) and isRight and self.controller.direction != "left"):
                self.controller.add_left()
            if (isRight and self.controller.direction == "right"):
                self.controller.rm_right()
            if (isLeft and self.controller.direction == "left"):
                self.controller.rm_left()
            if ((not isRight) and (not isLeft)):
                #stop the car (no lane)
                self.controller.rm_forward()
                if(self.controller.direction == "right"):
                    self.controller.rm_right()
                elif(self.controller.direction == "left"):
                    self.controller.rm_left()
            
        


if __name__ == "__main__":
    agent = Agent()
    agent.run()
