from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class Color(QWidget):
    def __init__(self,color):
        super(Color,self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window,QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()

        

        layout1 = QVBoxLayout()
        layout1.addWidget(Color('purple'))
        layout1.addWidget(Color('dark'))
        layout1.addWidget(Color('blue'))


        layoutOverallH = QHBoxLayout()
        layoutOverallH.addLayout(layout1)
        layoutOverallH.addWidget(Color('darkgreen'))

        widget = QWidget()
        widget.setLayout(layoutOverallH)

        self.setCentralWidget(widget)
        self.showGUI()
    
    def showGUI(self):
        self.setWindowTitle("Layouts")
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
