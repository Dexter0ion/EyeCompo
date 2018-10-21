from flask import Flask
from flask import request,render_template, Response,request
from Camera import Camera
import time
app = Flask(__name__)

frame = None
def gen():
    """Video streaming generator function."""
    while True:
        #frame = Camera.get_frame()
        #print("public frame frame type:"+str(type(frame)))
        fopen=[open('loaded.jpg', 'rb').read()]
        frame = fopen[0]
        time.sleep(0.1)
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save('loaded.jpg')
    return "upload"



app.run(port=5001)