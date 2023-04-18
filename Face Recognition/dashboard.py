from __future__ import print_function
import eel
import pyautogui
import cmake
import dlib
import numpy 
import face_recognition
import cv2
from views.models.login import login_user,login_session
from views.models.register import register_user
import os
from datetime import datetime
import numpy as np


eel.init('views')


@eel.expose
def display():
    imgElon = face_recognition.load_image_file('/Users/mananshah/Downloads/Face Recognition/Back-End/Elon_Musk_Royal_Society_(crop2).jpg')
    imgElon = cv2.cvtColor(imgElon,cv2.COLOR_BGR2RGB)

    imgTEST = face_recognition.load_image_file('/Users/mananshah/Downloads/Face Recognition/Back-End/230209152722-elon-musk-0127.jpeg')
    imgTEST = cv2.cvtColor(imgTEST,cv2.COLOR_BGR2RGB)


    faceLoc = face_recognition.face_locations(imgElon)[0]
    encodeElon = face_recognition.face_encodings(imgElon)[0]
    cv2.rectangle(imgElon,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)
    #print(faceLoc)
    faceLoc = face_recognition.face_locations(imgTEST)[0]
    encodeTEST = face_recognition.face_encodings(imgTEST)[0]
    cv2.rectangle(imgTEST,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)

    results = face_recognition.compare_faces([encodeElon],encodeTEST)
    faceDis = face_recognition.face_distance([encodeElon],encodeTEST)
    print(results, faceDis)

    cv2.putText(imgTEST,f'{results} {round(faceDis[0],2)}',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)


    cv2.imshow('FACE1',imgElon)
    cv2.imshow('FACE2',imgTEST)
    cv2.waitKey(0)
    
@eel.expose
def btn_login(username,password):
    
    msg=login_user(username,password)
    eel.login_return(str(msg))

@eel.expose
def btn_register(username,password,email):
    msg=register_user(username,password,email)
    eel.register_return(str(msg))

@eel.expose
def get_user_online():
    get_user=login_session()
    print(get_user)
    eel.get_user(str(get_user))


@eel.expose
def recognize():

    path = '/Users/mananshah/Downloads/Face Recognition/Back-End/C Batch'


    Images = []
    classNames = []
    

    myList = os.listdir(path)

    print(myList)

    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        Images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)

    def findEncodings(Images):
        encodeList =[]
        for img in Images:

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
    # print(encodeList)
        return encodeList
    
    def markAttendance(name):
        
        with open('/Users/mananshah/Downloads/Face Recognition/Back-End/ATTENDANCE.csv','r+') as f:
            myDataList = f.readlines()
            nameList = [] 
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')  

    encodeListKnown = findEncodings(Images)
    print('Encoding Complete')
    cap = cv2.VideoCapture(0)
    stop=False
    while True and stop==False:
        success, img = cap.read()
        #img = captureScreen()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            #print(faceDis)
            matchIndex = np.argmin(faceDis)

            # if matches[matchIndex]:
                # name = classNames[matchIndex].upper()
                # print(name)
                
            if faceDis[matchIndex]< 0.50: 
                name = classNames[matchIndex].upper()
                markAttendance(name)

            else: 
                name = 'Unknown'
            #cv2.imwrite(f"{name}.jpg", curImg )
            # face_recognition.update([curImg], [name])
            # face_recognition.write(path)
        
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)

            cv2.imshow('Webcam',img)
            k=cv2.waitKey(1)
            if(k==ord("q")):
                stop=True
    
    
    cv2.destroyAllWindows()

@eel.expose
def btn_save(i,file):
        
    print(i)
    directory = r'/Users/mananshah/Downloads/Face Recognition/Back-End/C Batch'

    # Load the image using OpenCV
    img = cv2.imread(i) 

    # Change the working directory to the specified directory for saving the image
    os.chdir(directory) 

    # Print the list of files in the directory before saving the image
    print("Before saving")   
    print(os.listdir(directory))   

    # Save the image with the filename "cat.jpg"
        
    cv2.imwrite(file,img) 

        # Print the list of files in the directory after saving the image
    print("After saving")  
    print(os.listdir(directory))
    
eel.start(
    'templates/login.html',size=pyautogui.size()
    )
