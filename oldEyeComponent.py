# code:utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
import cv2

from UICircleMain import Window


class UpdateFrame(QThread):
    """更新数据类"""
    update_date = pyqtSignal(str)  # pyqt5 支持python3的str，没有Qstring

    def run(self):
        cnt = 0
        while True:
            cnt += 1
            self.update_date.emit(str(cnt))  # 发射信号
            time.sleep(1)


class cameraOpen(QThread):

    def run(self):
        camera = cv2.VideoCapture(0)
        while camera.isOpened():
        #采集摄像头线程
            ret, vframe = camera.read()
            height, width, bytesPerComponent = vframe.shape
            bytesPerLine = bytesPerComponent * width
        # 变换彩色空间顺序
            cv2.cvtColor(vframe, cv2.COLOR_BGR2RGB, vframe)
        # 转为QImage对象
            self._qimage = QImage(vframe.data, width, height, bytesPerLine,
                        QImage.Format_RGB888)

            cv2.imshow("运动轮廓|contours", vframe)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        cv2.destroyAllWindows()
        camera.release()
        
    @property
    def Qimg(self):
        return self._qimage

    @property
    def QArray(self):
        return self._qimage



if __name__ == '__main__':
        camera = cameraOpen()
        camera.run()
        #camera.start()

        
        #实例化界面
        app = QApplication(sys.argv)
        EyeGUI = Window(camera.QArray)

        #更新线程
        #显示
        EyeGUI.show()
        app.exit(app.exec_())
        