#-*-coding:utf-8-*-
'''
    2018/5/15 Learning @property and assert statement
    Freddie Mercury is coooool！
'''
import cv2
import sys
import numpy as np
import time

from PyQt5.QtWidgets import QApplication
from UICircleMain import Window


class CaptureManager(object):
    def __init__(self,
                 capture,
                 preiviewWindowManager=None,
                 shouldMirrorPreview=False):
        self.preiviewWindowManager = preiviewWindowManager
        self.shouldMirrorPreview = shouldMirrorPreview

        self._capture = capture
        self._channel = 0
        self._enteredFrame = False

        self._frame = None
        self._imageFilename = None
        self._videoFilename = None
        self._videoENcoding = None
        self._videoWriter = None

        self._startTime = None
        self._frameElapsed = int(0)  # exchange long() to int()?
        self._fpsEstimate = None

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def chanel(self, value):
        if self._channel != value:
            self._channel = value
            self._frame = None

    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve(
            )  # what does retrieve() mean?
            return self._frame

    @property
    def isWritingImage(self):
        return self._imageFilename is not None

    @property
    def isWritingVideo(self):
        return self._videoFilename is not None

    def enterFrame(self):
        ''' Capture the next frame,if any.  
            捕获存在的下一帧
        '''
        # 首先检查先前帧是否存在
        #assert not self._enteredFrame
        #print("previous enterFrame had no matching exitFrame()")

        if self._capture is not None:


    def exitFrame(self):
        '''
        Draw to the window.
        Write to files.
        Release the frame.
        '''
        '''
        检测是有否可获取的帧图像
        The getter may retrieve and cache the frame
        '''

        if self._frame is None:
            self._enteredFrame = False
            return
        '''
        更新FPS以及相关变量
        '''
        if self._frameElapsed == 0:
            self._startTime = time.time()
        else:
            timeElapsed = time.time() - self._startTime
            self._fpsEstimate = self._frameElapsed / timeElapsed

        self._frameElapsed += 1
        '''
        绘制GUI
        '''
        if self.preiviewWindowManager is not None:
            if self.shouldMirrorPreview:
                # 镜像反转 Flip array in the left/right direction.
                mirroredFrame = np.fliplr(self._frame).copy()
                self.ndarray2qimage(mirroredFrame)
                self.preiviewWindowManager.showGUI(self._qimage)
            else:
                self.ndarray2qimage(self._frame)
                self.preiviewWindowManager.showGUI(self._qimage)
        '''
        保存图像
        '''
        if self.isWritingImage:
            cv2.imwrite(self._imageFilename, self._frame)
            self._imageFilename = None
        '''
        释放帧
        '''

        self._frame = None
        self._enteredFrame = False

    def writeImage(self, filename):
        self._imageFilename = filename
    
    def ndarray2qimage(self,frame):
        height, width, bytesPerComponent= frame.shape
        bytesPerLine = bytesPerComponent* width
        # 变换彩色空间顺序
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB,frame)
        # 转为QImage对象
        self._qimage= QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        


class GUIManager(object):
    def __init__(self, GUIName, keypressCallback=None):
        self.keypressCallback = keypressCallback
        self._GUIName = GUIName
        self._isGUICreated = False

    @property
    def isGUICreated(self):
        return self._isGUICreated

    def createGUI(self):

        self._isGUICreated = True

    def showGUI(self, frame):
        self._GUIApp = QApplication(sys.argv)
        self._GUIWindow = Window(imgpath=frame)
        self._GUIWindow.show()
        sys.exit(self._GUIApp.exec_())

    def destroyGUI(self):
        
        self._isGUICreated = False

    def preocessEvent(self):
        keycode = cv2.waitKey(1)

        if self.keypressCallback and keycode != -1:
            # Discard any non-ASCII info encoded by gtk
            # 舍弃所有由GTK编码的非ASCII信息
            keycode &= 0xFF
            self.keypressCallback(keycode)

def main():
    cm = CaptureManager(None)
    cm.enterFrame()
    print(cm.frame)
    print(cm.isWritingImage)
    print(cm.isWritingVideo)

    GM = GUIManager('test-window', True)
    cat_frame = open('cat.jpg', 'rb').read()
    c = cv2.VideoCapture(0)
    ret, vframe = c.read()
    height, width, bytesPerComponent= vframe.shape
    bytesPerLine = bytesPerComponent* width
    # 变换彩色空间顺序
    cv2.cvtColor(vframe, cv2.COLOR_BGR2RGB,vframe)
        # 转为QImage对象
    qimage= QImage(vframe.data, width, height, bytesPerLine, QImage.Format_RGB888)


    #vimg = Image.fromarray(vframe) 

    
    
    GM.showGUI(qimage)
    cv2.waitKey(0)
    GM.destroyGUI()
    


if __name__ == '__main__':
    main()
