from flask import Flask, Response
import numpy as np
import cv2
from PIL import ImageGrab
import time

# Initialize Flask app
app = Flask(__name__)

# Screen capture generator function
def capture_screen():
    """Capture the screen and serve as a video stream."""
    while True:
        # Capture the screen using ImageGrab (Pillow)
        screen = np.array(ImageGrab.grab())  # Capture the screen
        
        # Encode the screen as a JPEG image using OpenCV
        _, encoded_img = cv2.imencode('.jpg', screen)  # JPEG encode
        img_data = encoded_img.tobytes()  # Convert to bytes
        
        # Yield the image in multipart response (MJPEG stream)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img_data + b'\r\n\r\n')
        time.sleep(0.1)  # Control frame rate (10 FPS)

@app.route('/')
def index():
    """Render the main page with the video stream."""
    return '''
        <html>
            <body>
                <h1>Live Screen Stream</h1>
                <img src="/video_feed" />
            </body>
        </html>
    '''

@app.route('/video_feed')
def video_feed():
    """Video feed that continuously sends screen captures."""
    return Response(capture_screen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Start the Flask app on localhost and port 5000
    app.run(host='127.0.0.1', port=5000, threaded=True)
