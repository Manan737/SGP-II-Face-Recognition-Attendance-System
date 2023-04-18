import cmake
import dlib
import numpy 
import face_recognition
import cv2
    
imgElon = face_recognition.load_image_file('FACE1.jpg')
imgElon = cv2.cvtColor(imgElon,cv2.COLOR_BGR2RGB)

imgTEST = face_recognition.load_image_file('FACE2.jpg')
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