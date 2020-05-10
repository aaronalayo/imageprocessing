import numpy as np
import cv2

def face_detect():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    img = cv2.imread('people.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    image_copy = np.copy(img)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        # eyes = eye_cascade.detectMultiScale(roi_gray)
        # for (ex,ey,ew,eh) in eyes:
        # cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow('img',img)

    cv2.waitKey() & 0xFF

    # Press ecs to quit
    cv2.destroyAllWindows()
    



def crop_face():
    
    face_crop = []
    for f in faces:
        x, y, w, h = [ v for v in f ]
        cv2.rectangle(image_copy, (x,y), (x+w, y+h), (255,0,0), 3)
        # Define the region of interest in the image  
        face_crop.append(img[y:y+h, x:x+w])

    for face in face_crop:
        cv2.imshow('face',face)
        cv2.waitKey(0)
    
# print('Number of faces detected:', len(faces))


if __name__ == "__main__":
    face_detect()
