from flask import Flask, render_template, Response,request
import requests
import cv2
import os,sys
'''
    issue:类公共变量存储视频帧
'''
class NetCompo:
    app = Flask(__name__)
    frame = None

    
    def gen():
        """Video streaming generator function."""
        while True:
            #frame = imgdata
            #print("NetCompo.frame type:"+str(type(NetCompo.frame)))
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + NetCompo.frame + b'\r\n')
            #print(NetCompo.frame)
    

    @app.route('/')
    def index():
            return render_template('index.html')
    
    @app.route('/shutdown',methods=['POST'])
    def shutdown():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    @app.route('/video_feed')
    def video_feed():
        """Video streaming route. Put this in the src attribute of an img tag."""
        print(type(NetCompo.gen()))
        return Response(NetCompo.gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


    
    def setFrame(self,imgdata):
        #self.frame = imgdata
        
        #numpy.ndarray to bytes
        NetCompo.frame=cv2.imencode('.jpg', imgdata)[1].tobytes()
        
        #print(self.frame)
    
    def oneShotPost2Server(self):
        self.postFrame2Server('http://localhost:5001/upload',NetCompo.frame)

    '''
    def shutdown(self):
        raise RuntimeError("Server going down")
    '''
    def run(self):
        self.app.run(threaded=True)
        
        '''
        try:
            self.app.run(threaded=True)
        except (RuntimeError, msg):
            if str(msg) == "Server going down":
                pass # or whatever you want to do when the server goes down
            else:
                pass
        '''
        
    
    def stop(self):
        #self.shutdown() 
        requests.post('http://localhost:5000/shutdown')
    
    def testPosttoServer(self):
        url = 'http://localhost:5001/upload'
        files = {'file':('1.jpg',open('1.jpg','rb'))}
        requests.post('http://localhost:5001/upload',files=files)

    def postFrame2Server(self,url,frame):
        files = {'file':('1.jpg',frame)}
        requests.post(url,files=files)

    



