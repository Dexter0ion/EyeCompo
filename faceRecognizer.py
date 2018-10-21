import cv2
import numpy as np
import os


class faceRecognizer:
    def __init__(self, cam):
        # 加载先前训练的面部识别器
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('trainer/trainer.xml')

        # 加载面部级联分类器
        self.cascadePath = "cascades/haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascadePath)

        # 显示字体
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        # 姓名标记 Master：0
        self.names = ['Master', 'juju']

        # 定义最小面部识别大小
        self.minW = 0.1*cam.get(3)
        self.minH = 0.1*cam.get(4)

    def loadTest(self):
        print("imported!")

    def recognize(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(self.minW), int(self.minH)),
        )
        for(x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])

            # Check if confidence is less them 100 ==> "0" is perfect match
            if (confidence < 100):
                id = self.names[id]
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))

            cv2.putText(img, str(id), (x+5, y-5),
                        self.font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence), (x+5, y+h-5),
                        self.font, 1, (255, 255, 0), 1)

        return img
