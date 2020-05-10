import tkinter as tk
import cv2
from tkinter import Frame, Tk, BOTH, Text, Menu, END, filedialog, Label, Canvas
from PIL import ImageTk, Image
import numpy as np
import os



class ImageProcessor(Frame):


    def __init__(self, parent):
        Frame.__init__(self, parent)   

        self.parent = parent        
        self.initUI()

    def initUI(self):

        self.parent.title("Image Processor")
        self.pack(fill=BOTH, expand=1)

        filebar = Menu(self.parent)
        self.parent.config(menu=filebar)
      

        fileMenu = Menu(filebar)
        filebar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Open", command=self.open_img)
        fileMenu.add_command(label="Save", command =self.save_img)

        editMenu = Menu(filebar)
        filebar.add_cascade(label= "Edit", menu= editMenu)
        editMenu.add_command(label="Undo")

        imageMenu = Menu(filebar)
        filebar.add_cascade(label= "Image", menu= imageMenu)
        imageMenu.add_command(label= "Rotate Right", command= self.rotate_right_img)
        imageMenu.add_command(label= "Rotate Left", command= self.rotate_left_img)
        imageMenu.add_command(label= "Resize")
        imageMenu.add_command(label= "Face detection", command= self.face_detect)

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)
    
    def openfn(self):
        filename = filedialog.askopenfilename(title='open')
        return filename


    def open_img(self):
        self.cv2img = cv2.imread(self.openfn())
        self.cv2img = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2RGB)

        scale_percent = 50 # percent of original size
        width = int(self.cv2img.shape[1] * scale_percent / 100)
        height = int(self.cv2img.shape[0] * scale_percent / 100)
        dim = (width, height)
        self.cv2img = cv2.resize(self.cv2img, dim, interpolation = cv2.INTER_AREA)
        image = Image.fromarray(self.cv2img)
        image = ImageTk.PhotoImage(image)
        self.panel = Label(root, image = image)
        self.panel.image = image
        self.panel.pack(fill=BOTH, expand=True)
        self.panel.place(x = 0, y= 0)

    def rotate_right_img(self):

        self.cv2img = cv2.rotate(self.cv2img, cv2.ROTATE_90_CLOCKWISE)
        rotated = Image.fromarray(self.cv2img)
        rotated = ImageTk.PhotoImage(rotated)
        self.panel.configure(image = rotated)
        self.panel.image = rotated

    def rotate_left_img(self):

        self.cv2img = cv2.rotate(self.cv2img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        rotated = Image.fromarray(self.cv2img)
        rotated = ImageTk.PhotoImage(rotated)
        self.panel.configure(image = rotated)
        self.panel.image = rotated

    def save_img(self):
        save_img = Image.fromarray(self.cv2img)
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if filename is None:
           return
        save_img.save(filename)
        
    def face_detect(self):
        face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
       
        gray = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2GRAY)


        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            self.cv2img = cv2.rectangle(self.cv2img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = self.cv2img[y:y+h, x:x+w]
            # eyes = eye_cascade.detectMultiScale(roi_gray)
            # for (ex,ey,ew,eh) in eyes:
            # cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        cv2.imshow('Press esc to exit',self.cv2img)
        cv2.waitKey() & 0xFF
        cv2.destroyAllWindows()

    def exitProgram(self):
        os._exit(0)

if __name__ == '__main__':

    root=Tk()
    ph=ImageProcessor(root)
    root.geometry("900x600")
    root.mainloop()
