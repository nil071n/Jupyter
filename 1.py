from flask import Flask, Response
import numpy as np
import cv2
from PIL import ImageGrab
import time

# Create Flask app
app = Flask(__name__)

def capture_screen():
    """Capture the screen continuously and send it to the client."""
    while True:
        # Capture the screen using ImageGrab
        screen = np.array(ImageGrab.grab())
        
        # Convert the screen capture to a byte array using OpenCV
        _, encoded_img = cv2.imencode('.jpg', screen)  # JPEG encode
        img_data = encoded_img.tobytes()  # Convert to bytes
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img_data + b'\r\n\r\n')
        time.sleep(0.1)  # Sleep to reduce load and control frame rate

@app.route('/video_feed')
def video_feed():
    """Route that serves the screen image as a video feed"""
    return Response(capture_screen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """Serve the main page that displays the video feed"""
    return '''
        <html>
            <body>
                <h1>Live Screen Feed</h1>
                <img src="/video_feed" />
            </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, threaded=True)
