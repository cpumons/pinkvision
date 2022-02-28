import cv2, time
import requests
import numpy as np
from flask import Flask, render_template, Response

app = Flask(__name__)


# url = "http://192.168.1.34:8080/shot.jpg"
webcam = cv2.VideoCapture(0)
a=0

"""img_resp = requests.get(url)
img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
imgOriginalScene = cv2.imdecode(img_arr, -1)"""

def gen_frames():  
    while True:
        success, frame = webcam.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

cv2.destroyAllWindows()

app.run(debug=True, host="0.0.0.0", port=50000)
