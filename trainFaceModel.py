import cv2
import numpy as np
from PIL import Image
import os

#面部数据集
path = 'facedata'

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("cascades/haarcascade_frontalface_default.xml")

#获取图像和标记数据

def getImageAndLabels(path):

    #合并目录 一个list
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)] 
    faceSamples = []
    ids = []

    for iPath in imagePaths:
        PIL_img = Image.open(iPath).convert('L')
        img_numpy = np.array(PIL_img,'uint8')

        #获取标签及面部特征
        id = int(os.path.split(iPath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
            
    return faceSamples,ids
print ("\n [INFO] 面部数据训练中...|Training faces. It will take a few seconds. Wait ...")
faces,ids = getImageAndLabels(path)
recognizer.train(faces, np.array(ids))
print ("\n [Success] 训练完成|Training Complete")
print ("\n [Writing] 写出外部数据中...")
recognizer.save('trainer/trainer.yml') 
recognizer.save('trainer/trainer.xml') 
print ("\n [Success] 写出完成|Writing Complete")