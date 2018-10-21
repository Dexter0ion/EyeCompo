import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
'''
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QBrush, QImage, QPainter, QPixmap, QWindow
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget,QGridLayout
'''
'''
    from https://stefan.sofa-rockers.org/2018/05/04/how-to-mask-an-image-with-a-smooth-circle-in-pyqt5/


Return a ``QPixmap`` from *imgdata* masked with a smooth circle.

*imgdata* are the raw image bytes, *imgtype* denotes the image type.
The returned image will have a size of *size* × *size* pixels.

'''


def mask_image(imgdata, imgtype='jpg', size=400):
    # Load image and convert to 32-bit ARGB (adds an alpha channel):
    #image = QImage.fromData(imgdata, imgtype)
    image = imgdata
    image.convertToFormat(QImage.Format_ARGB32)

    # 将图像切割为正方形
    imgsize = min(image.width(), image.height())
    rect = QRect(
        (image.width() - imgsize) / 2,
        (image.height() - imgsize) / 2,
        imgsize,
        imgsize,
    )

    image = image.copy(rect)

    # 以相同维度和alpha channel创建输出图像
    # 透明化

    out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
    out_img.fill(Qt.transparent)

    # 创建texture brush 画圆 onto out_img
    brush = QBrush(image)  # 创建texture brush
    painter = QPainter(out_img)
    # 设置painter
    painter.setBrush(brush)
    painter.setPen(Qt.NoPen)  # 无边框
    painter.setRenderHint(QPainter.Antialiasing, True)  # 抗锯齿
    painter.drawEllipse(0, 0, imgsize, imgsize)  # 画圆
    painter.end()  # segfault if you forget this

    # 将image转换为pixmap病重定义大小
    # 设置分辨率适应高清屏
    pr = QWindow().devicePixelRatio()
    pm = QPixmap.fromImage(out_img)
    pm.setDevicePixelRatio(pr)
    size *= pr
    pm = pm.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    return pm


class Color(QWidget):
    def __init__(self,color):
        super(Color,self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window,QColor(color))
        self.setPalette(palette)


class QSwitchButton(QPushButton):
    switchSignal = pyqtSignal(str)
    def __init__(self,onasset,offasset):
        

        super().__init__()
        self.switchName = ""
        self.onasset = onasset
        self.offasset = offasset
        self.setStyleSheet('QPushButton{border-image:url('+self.offasset+')}')
        #self.setStyleSheet('QPushButton{background-image:url('+self.offasset+')}')
        self.isoff = True
        self.clicked.connect(self.changeSwitchButtonImage)
        self.clicked.connect(self.clieckedCallFunction)
    
    def setSwitchName(self,switchName):
        self.switchName = switchName
        

    def clieckedCallFunction(self):
        print(self.sender().switchName+"is cliecked")

    def changeSwitchButtonImage(self):
        print("Pushbutton Image changed")
        if self.isoff:
            #self.setStyleSheet('QPushButton{background-image:url('+self.onasset+')}')
            self.setStyleSheet('QPushButton{border-image:url('+self.onasset+')}')
            self.switchSignal.emit("on")
            self.isoff = False
        elif self.isoff == False:
            #self.setStyleSheet('QPushButton{background-image:url('+self.offasset+')}')
            self.setStyleSheet('QPushButton{border-image:url('+self.offasset+')}')
            self.switchSignal.emit("off")
            self.isoff = True

    


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initGUI()

    def initGUI(self):
        # 读取QImage格式图像
        self._imgdata = QImage()
        self._pixmap = QPixmap()
        self._imgtext = ""

        # 界面布局
        self.ilabel = QLabel()
        self.ilabel.setPixmap(self._pixmap)
        self.tlabel = QLabel(self._imgtext)


        self.layoutU = QVBoxLayout()
        self.layout = QHBoxLayout()

        
        self.layoutL = QVBoxLayout()
        self.layoutM = QVBoxLayout()

        self.layoutMDown = QHBoxLayout()

        self.layoutR  = QVBoxLayout()



        #central down dial
        self.dial = QDial()
        self.dial.setProperty("value", 30)
        self.dial.setObjectName("dial")

        self.slider = QSlider()
        self.btnl = QPushButton()
        
        #self.btnl.setIcon(QIcon("assets/switch-pre-off"))
        self.btnl.setFixedSize(75,150)
        #self.btnl.setStyleSheet('QPushButton{border-image:url(assets/switch-pre-off.png)}')
        self.btnl.setStyleSheet('QPushButton{background-image:url(assets/switch-pre-off-small.png)}')
        
        self.swbtn0 = QSwitchButton("assets/cola_red_on_right.png","assets/cola_red_off_right.png")
        self.swbtn1 = QSwitchButton("assets/cola_red_on_right.png","assets/cola_red_off_right.png")
        self.swbtn2 = QSwitchButton("assets/cola_red_on_right.png","assets/cola_red_off_right.png")
        self.swbtn3 = QSwitchButton("assets/cola_red_on_right.png","assets/cola_red_off_right.png")
        #self.swbtn2 = QSwitchButton("assets/switch-pre-on.png","assets/switch-pre-off.png")
        #self.swbtn3 = QSwitchButton("assets/switch-pre-on.png","assets/switch-pre-off.png")
        swbtnArr = [self.swbtn0,self.swbtn1,self.swbtn2,self.swbtn3]

        #self.layoutMDown.addWidget(self.dial)
        self.layoutMDown.setSpacing(0)
        for swbtn in swbtnArr:
            swbtn.setFixedSize(100,100)
            self.layoutMDown.addWidget(swbtn)

        self.swbtn0.setSwitchName("NET-SWITCH")
        #add panel
        self.panel = QSwitchButton("assets/PanaPanel.png","assets/PanaPanel.png")
        self.panel.setFixedSize(400,120)
        self.layoutL.addWidget(Color('purple'))

        self.layoutM.addWidget(self.ilabel)


        self.layoutMDown.addWidget(self.slider)
        self.layoutM.addLayout(self.layoutMDown)
        self.layoutR.addWidget(self.panel)
       #self.layoutM.addWidget(Color('brown'))
        self.layoutR.addWidget(Color('grey'))
        self.layoutR.addWidget(Color('brown'))




        
        self.layout.addLayout(self.layoutL)
        self.layout.addLayout(self.layoutM)
        self.layout.addLayout(self.layoutR)
        
        '''
        self.layout = QGridLayout()
        self.layout.addWidget(self.ilabel, 0, 2)
        #self.layout.addWidget(Color('dark'),0,0,2,2)
        self.layout.addWidget(Color('grey'),0,0,1,1)
        '''
        self.setLayout(self.layout)

    def updateFrame(self, imgdata):
        self._imgdata = imgdata
        # 转换为圆形
        self._pixmap = mask_image(self._imgdata)

        #照常输出

        self.ilabel.setPixmap(self._pixmap)
        # self.layout.addWidget(self.ilabel,0,Qt.AlignCenter)

    def updateText(self, imgtext):
        self._imgtext = imgtext
        self.tlabel.setText(self._imgtext)
        #self.layout.addWidget(self.tlabel, 0, Qt.AlignCenter)
    
    def getSwitchSignal(self,swsignal):
        s = swsignal
        print(s)
    
    