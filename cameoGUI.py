import cv2
from managersGUI import GUIManager, CaptureManager


class Cameo(object):
    def __init__(self):
        self._GUIManager = GUIManager('Cameo', self.onKeypress)
        self._captureManager = CaptureManager(
            cv2.VideoCapture(0), self._GUIManager, True)

    def run(self):
        '''
        主函数循环
        '''
        self._GUIManager.createGUI()
        while self._GUIManager.isGUICreated:
            '''
            进入帧
            '''
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            '''
            目标：处理帧
            '''
            '''
            结束帧
            '''
            self._captureManager.exitFrame()
            self._GUIManager.preocessEvent()

    def onKeypress(self, keycode):
        '''
        监测按键
        SPACE 截屏
        TAB   开始/停止录制视频
        ESC   退出
        '''

        if keycode == 32:  # SPACE
            self._captureManager.writeImage('screenshot.png')

        elif keycode == 27:  # ESC
            self._GUIManager.destroyWindow()


if __name__ == "__main__":
    Cameo().run()
