# code:utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
import cv2

from UICircleMain import Window
from faceRecognizer import faceRecognizer
from NetCompo import NetCompo

import threading
import numpy

'''
    use ProcessThread will lower the speed a lot!
    10/11
'''

class ProcessThread(QThread):
    origFrame = None
    procFrame = None

    isFaceOpen = True

    update_procFrame = pyqtSignal(numpy.ndarray)

    def __init__(self):
        super().__init__()
        self.initFaceRecog()

    def initFaceRecog(self):
        # 初始化面部识别类
        self.faceR = faceRecognizer("nocamera")
        self.faceR.loadTest()
    
    def procFaceRecog(self,newframe):
        faceProcFrame = self.faceR.recognize(newframe)
        return faceProcFrame

    def getOrigFrame(self,origFrame):
        #print("get origin frame")
        self.origFrame = origFrame
        self.procFrame = self.origFrame


        if self.isFaceOpen == True:
            #print("process frame")
            self.procFrame = self.procFaceRecog(self.procFrame)
        elif self.isFaceOpen == False:
            self.procFrame = self.procFrame

        #print("emit processed frame")
        self.update_procFrame.emit(self.procFrame)
    '''
    def processFrame(self):
        print("process frame")
        if self.isFaceOpen == True:
            self.procFrame = self.procFaceRecog(self.procFrame)
        elif self.isFaceOpen == False:
            self.procFrame = self.procFrame





    def emitProcFrame(self):
        if self.procFrame != None:
            self.update_procFrame.emit(self.procFrame)
    '''
    def getFaceSwitchSignal(self,swsignal):
        s = swsignal
        if s=="on":
            self.isFaceOpen = True
        elif s=="off":
            self.isFaceOpen = False
        print(s)

    def run(self):
        pass




class CaptureThread(QThread):

    update_imgtext = pyqtSignal(str)
    update_imgdata = pyqtSignal(QImage)
    update_cvimgdata = pyqtSignal(numpy.ndarray)

    #send_origFrame = pyqtSignal(numpy.ndarray)
    camera = cv2.VideoCapture(1)

    isFaceOpen = True

    def __init__(self):
        super().__init__()
        self.initFaceRecog()

    def initFaceRecog(self):
        # 初始化面部识别类
        self.faceR = faceRecognizer(self.camera)
        self.faceR.loadTest()
    
    def procFaceRecog(self,newframe):
        faceProcFrame = self.faceR.recognize(newframe)
        return faceProcFrame

    def processFrame(self):
        #print("process frame")
        if self.isFaceOpen == True:
            self._frame = self.procFaceRecog(self._frame)

    def getFaceSwitchSignal(self,swsignal):
        s = swsignal
        if s=="on":
            self.isFaceOpen = True
            print("Face Switch On")

        elif s=="off":
            self.isFaceOpen = False
            print("Face Switch Off")

        
    def run(self):

        while self.camera.isOpened():
            #print("capture")
            # 采集摄像头线程
            ret, self._frame = self.camera.read()

            # 处理帧
            self.processFrame()
            
            #发送原始图像帧
            #self.send_origFrame.emit(self._frame)

            self._frameQ = self.cvtNdarry2QImage(self._frame)
            self.update_imgdata.emit(self._frameQ)

            cv2.cvtColor(self._frame, cv2.COLOR_BGR2RGB, self._frame)
            self.update_cvimgdata.emit(self._frame)
            # time.sleep(0.05)

        self.camera.release()

    '''
    def getProcessFrame(self,procFrame):
            self._frame = procFrame
    '''
    def cvtNdarry2QImage(self, ndarray):
        # in this class ndarry meands frame capture image
        vframe = ndarray    
        # 采集摄像头线程
        height, width, bytesPerComponent = vframe.shape
        bytesPerLine = bytesPerComponent * width
        # 变换彩色空间顺序
        cv2.cvtColor(vframe, cv2.COLOR_BGR2RGB, vframe)
        qimg = QImage(vframe.data, width, height,
                      bytesPerLine, QImage.Format_RGB888)
        return qimg


class NetThread(QThread):
    netcompo = NetCompo()
    def run(self):
        print("[开启]Flask服务器线程")
        self.netcompo.run()
    
    def stop(self):
        print('[关闭]Flask服务器')
        self.netcompo.stop()

    def updateFrame(self,imgdata):
        #print("更新服务器画面帧")
        #print(imgdata)
        self.netcompo.setFrame(imgdata)
        #self.netcompo.testPosttoServer()
    
    def getSwitchSignal(self,swsignal):
        s = swsignal
        print(s)

class ThreadMana:
    # 开启FLask服务端线程
    netThread = NetThread()
    def getNetSwitchSignal(self,swsignal):
        s = swsignal
        if s=="on":
            self.netThread.start()
        elif s=="off":

            self.netThread.stop()

        print(s)
    


if __name__ == '__main__':
    
    # 实例化窗口
    app = QApplication(sys.argv)
    CameoGUI = Window()

    threadMana = ThreadMana()
    #procThread = ProcessThread()
    #procThread.start()

    # 开启FRAME捕获线程
    cameoThread = CaptureThread()
    # cameoThread.update_imgtext.connect(CameoGUI.updateText)
    cameoThread.update_imgdata.connect(CameoGUI.updateFrame)
    cameoThread.update_cvimgdata.connect(threadMana.netThread.updateFrame)
    cameoThread.start()
    
    #cameoThread.send_origFrame.connect(procThread.getOrigFrame)
    #procThread.update_procFrame.connect(cameoThread.getProcessFrame)
    

    #界面SWitch按钮信号测试
    CameoGUI.swbtn0.switchSignal.connect(threadMana.getNetSwitchSignal)
    CameoGUI.swbtn1.switchSignal.connect(cameoThread.getFaceSwitchSignal)

    # 显示窗口
    CameoGUI.resize(800,600)
    CameoGUI.show()
    app.exit(app.exec_())
    

    



 

