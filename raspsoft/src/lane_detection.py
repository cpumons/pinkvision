import warnings
import cv2
import numpy as np
import time
#https://medium.com/analytics-vidhya/building-a-lane-detection-system-f7a727c6694

"""
Lane detection system for autonomous driving.
"""

np.seterr(all="ignore")
warnings.filterwarnings("ignore")

class Road_info():
    """
    This class is used as an interface between the lane detection system and the autonomous driving system agent.
    """
    def __init__(self, lanes):
        self.lanes_array = lanes
        self.left_lane = []
        self.right_lane = []
        self.is_road = False
        if (len(lanes[0])>0) and (lanes[0][0] >= -50):
            #left lane is detected
            self.left_lane = lanes[0]
        if (len(lanes[1]) > 0) and (lanes[1][0] >= -50 and lanes[1][0] < 700):
            #right lane is detected
            #if right lane x coordinate exceed 700 (treshold), then we do not keep it.
            #idem for left lane with treshold
            self.right_lane = lanes[1]
        if (len(self.left_lane) != 0 and len(self.right_lane) != 0):
            self.is_road = True

def gauss(img, kernel_size=5):
    """
    Applies a Gaussian Noise kernel. (reducing noise)
    """
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def hsv_convert(img):
    """
    Convert RGB to HSV
    HSV tolerates light fluctuations
    """
    return cv2.cvtColor(img, cv2.COLOR_RGB2HSV)


def color_mask(image):
    """
    Applies a color mask to the image in HSV.
    """
    sensitivity = 120 #treshold (higher value => more colors will be detected)
    lower_white = np.array([0,0,255-sensitivity])
    upper_white = np.array([255,sensitivity,255])
    mask = cv2.inRange(image, lower_white, upper_white)
    return mask

def canny(image, low_threshold, high_threshold):
    """
    Applies the Canny edge detection method.
    """
    return cv2.Canny(image, low_threshold, high_threshold)

def region_mask(image):
    """
    Applies a rectangle mask to the image.
    We only keep 1/3 of the image.
    """
    height, width = image.shape[:2]
    rect = np.array([[(0,height), (width, height), (width, 2*height/3), (0, 2*height/3)]], dtype=np.int32)
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, rect, 255)
    masked = cv2.bitwise_and(image, mask)
    return masked

def average(image, lines):
    """
    Average the slopes and intercepts of all lines.
    """
    left = []
    right = []    
    if (isinstance(lines, np.ndarray)):
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            y_int = parameters[1]
            if slope < 0:
                left.append((slope, y_int))
            else:
                right.append((slope, y_int))
    if (len(right) != 0):
        right_avg = np.average(right, axis=0)
        right_line = make_points(image, right_avg)
    else: 
        #No right line detected
        right_line = []
    if (len(left) != 0):
        left_avg = np.average(left, axis=0)
        left_line = make_points(image, left_avg)
    else:
        #No left line detected
        left_line = []
    return np.array([left_line, right_line])


def display_lines(image, lines):
    """
    Display the lines on the original image.
    """
    lines_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            if (len(line) != 0):
                x1, y1, x2, y2 = line
                cv2.line(lines_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return lines_image

def make_points(image, average): 
    """
    Create list of points from a line represented by its coefficients.
    """
    slope, y_int = average 
    y1 = image.shape[0]
    y2 = int(y1 * (3/5))
    x1 = int((y1 - y_int) // slope)
    x2 = int((y2 - y_int) // slope)
    return np.array([x1, y1, x2, y2])

def get_lane_lines(image):
    """
    Executes the pipeline and returns the left and right lane lines. 
    Return negative values if no lane lines are detected and lane position otherwise.
    The lane position is represented as two points (x, y) which are the top and bottom of the lane.
    """
    image = gauss(image)
    hsv_image = hsv_convert(image)
    masked = color_mask(hsv_image)
    edges = canny(masked, 50, 150)
    region = region_mask(edges)
    lines = cv2.HoughLinesP(region, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = average(image, lines)
    return Road_info(averaged_lines)

if __name__ == "__main__":
    image = cv2.imread('img1.jpg')

    #start = time.time()
    road_info = get_lane_lines(image)
    #end = time.time()
    #print("Time taken: ", end - start)

    black_lines = display_lines(image, road_info.lanes_array)
    lanes_image = cv2.addWeighted(image, 0.9, black_lines, 1, 1)

    cv2.imshow('result', lanes_image)
    while(1):
        k = cv2.waitKey(33)
        if k==27:    # Esc key to stop
            break
    cv2.destroyAllWindows()


