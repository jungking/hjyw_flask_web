import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO
import base64

def show_image(image):
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    #image = 'C:/Users/immen/바탕 화면/github/python_web/app/image.jpg'                 #이미지 불러오기 해야함.
    ff = np.frombuffer(image, np.uint8)               #경로 한글 있으면 에러
    #image = image.astype('uint8')
    image = cv2.imdecode(ff, cv2.IMREAD_UNCHANGED)
    #cv2.imshow("1", image)
    image = cv2.resize(image, dsize=(400, 400), interpolation=cv2.INTER_LINEAR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("2", gray)
    faces = faceCascade.detectMultiScale(gray,
                                        scaleFactor= 1.3,      # 이미지 피라미드 스케일 factor
                                        minNeighbors=5,         # 인접 객체 최소 거리 픽셀
                                        minSize = (20,20)
                                        )        

    print ("Found {0} faces!".format(len(faces)))
    facelist=[[0,0,0,0]*len(faces)]
    print(facelist)
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 3)
        for i in range(len(faces)):
            facelist[i][0] = x
            facelist[i][1] = y
            facelist[i][2] = w
            facelist[i][3] = h
    print(facelist)
    if len(cv2.split(image))<=3:
        b, g, r = cv2.split(image)
        image = cv2.merge([r,g,b]) 
    #image = cv2.resize(image, dsize=(0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    #image = cv2.resize(image, dsize=(400, 400), interpolation=cv2.INTER_LINEAR)
    #cv2.imshow("Faces found", image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    rawBytes = BytesIO()
    img_buffer = Image.fromarray(image.astype('uint8'))
    img_buffer.save(rawBytes, 'PNG')
    rawBytes.seek(0)
    base64_img = base64.b64encode(rawBytes.read())
    facelen = len(faces)
    return base64_img,facelen,facelist

# 멀리 있는 얼굴 인식률 떨어짐 거의 20%..