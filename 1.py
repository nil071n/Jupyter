from flask import Flask, Response
import numpy as np
import cv2
from PIL import ImageGrab
import time

app = Flask(__name__)

def capture_screen():
    """Capture the screen and yield frames for MJPEG streaming."""
    while True:
        # Take a screenshot of the full screen
        screen = np.array(ImageGrab.grab())

        # Convert RGB (Pillow) to BGR (OpenCV)
        screen_bgr = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

        # Encode the image as JPEG
        success, buffer = cv2.imencode('.jpg', screen_bgr)
        if not success:
            continue

        # Convert to bytes and yield in MJPEG format
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        # Limit frame rate (~10 FPS)
        time.sleep(0.1)

@app.route('/')
def index():
    """Home page with embedded screen feed."""
    return '''
        <html>
            <head><title>Live Screen Stream</title></head>
            <body>
                <h1>Live Screen Stream</h1>
                <img src="/video_feed" width="100%" />
            </body>
        </html>
    '''

@app.route('/video_feed')
def video_feed():
    """Video feed route."""
    return Response(capture_screen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Run the app on all interfaces so other devices can access it
    app.run(host='0.0.0.0', port=5000, threaded=True)
