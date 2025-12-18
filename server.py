"""
sudo apt update
sudo apt install python3-pip
sudo apt install x11-utils
sudo pip3 install Flask Pillow
si marche pas pip install (module) --break-system-packages
"""

import io
import time
from PIL import ImageGrab
from flask import Flask, Response

app = Flask(__name__)

def capture_screen():
    """Capture the screen using PIL (Pillow)"""
    screen = ImageGrab.grab() 
    # screen = screen.resize((640, 480)) si lag
    
    img_byte_arr = io.BytesIO()
    screen.save(img_byte_arr, format="JPEG", quality=50) 
    img_byte_arr.seek(0)
    return img_byte_arr

@app.route('/stream')
def stream():
    """Stream the screen continuously to the browser"""
    def generate():
        while True:
            img_byte_arr = capture_screen()
            yield (b'--frame\r\n'
                   b'Content-Type: image/png\r\n\r\n' + img_byte_arr.read() + b'\r\n\r\n')
            time.sleep(1/20) # fps, par exemple 1/10 = 10 fps
    
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """Serve the HTML page that will display the stream"""
    return '''
        <html>
            <body>
                <h1>Raspberry Pi Screen Stream</h1>
                <img src="/stream" width="100%">
            </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
