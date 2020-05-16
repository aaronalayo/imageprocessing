import tkinter as tk
import cv2
from tkinter import Frame, Tk, BOTH, Text, Menu, END, filedialog, Label, Button
from PIL import ImageTk, Image
import numpy as np
import os
import filters

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
        imageMenu.add_command(label= "Crop 4:3", command= self.crop_img)
        imageMenu.add_command(label= "Face detection", command= self.face_detect)

        filtersMenu = Menu(filebar)
        filebar.add_cascade(label= "Filters", menu= filtersMenu)
        filtersMenu.add_command(label= "Dither", command= self.call_filters_ditter)

        self.btn = Button(root, text = 'Crop faces', command = self.crop_face)
        self.btn.pack_forget()

        self.panel = Label(root)
        self.panel.place(relx=.5, rely=.5, anchor="c")
        
        
        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)

        
    def openfn(self):
        filename = filedialog.askopenfilename(title='open')
        return filename

    def open_img(self):
        self.cv2img = cv2.imread(self.openfn())
        self.cv2img = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2RGB)

        width_original = int(self.cv2img.shape[1])
        height_original = int(self.cv2img.shape[0])
        aspectRatio = width_original/height_original
        height_new = 500
        width_new = int(height_new*aspectRatio)
        dim = (width_new, height_new)
        self.cv2img = cv2.resize(self.cv2img,dim, interpolation = cv2.INTER_AREA)
        image = Image.fromarray(self.cv2img)
        image = ImageTk.PhotoImage(image)
    
        self.panel.configure(image = image)
        self.panel.image = image

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

    def call_filters_ditter(self):
        self.cv2img = filters.convert_dithering(self.cv2img)
        filtered = Image.fromarray(self.cv2img)
        filtered = ImageTk.PhotoImage(filtered)
        self.panel.configure(image = filtered)
        self.panel.image = filtered
        

    def save_img(self):
        save_img = Image.fromarray(self.cv2img)
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if filename is None:
           return
        save_img.save(filename)
        
    def face_detect(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        self.gray = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2GRAY)
        self.cv2img = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2RGB)
       
        faces = self.face_cascade.detectMultiScale(self.gray, 1.3, 5)
        for (x, y, w, h) in faces:
            self.cv2img = cv2.rectangle(self.cv2img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            #roi_gray = gray[y:y+h, x:x+w]
            #roi_color = self.cv2img[y:y+h, x:x+w]
        
        self.cv2img = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2RGB)
        faceimg = Image.fromarray(self.cv2img)
        faceimg = ImageTk.PhotoImage(faceimg)
        self.panel.configure(image = faceimg)
        self.panel.image = faceimg
        
        self.btn.pack(side = 'right')
        
    def crop_face(self):
        faces = self.face_cascade.detectMultiScale(self.gray, 1.3, 5)
        self.cv2img = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2RGB)
        face_crop = []
        for f in faces:
            x, y, w, h = [ v for v in f ]
            #cv2.rectangle(self.cv2img, (x,y), (x+w, y+h), (255,0,0), 3)
            # Define the region of interest in the image  
            face_crop.append(self.cv2img[y:y+h, x:x+w])

        for face in face_crop:
            cv2.imshow('Press s to save cropped image',face)
            self.cv2img = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2RGB)
            k = cv2.waitKey(0) & 0xFF
            if k == 27:         # wait for ESC key to exit
                cv2.destroyAllWindows()
            elif k == ord('s'): # wait for 's' key to save and exit
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                save_img = Image.fromarray(face)
                filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
                save_img.save(filename)
                cv2.destroyAllWindows()
            
    def crop_img(self):
        self.cv2img = self.cv2img[0:400, 0:300]
        crop_image = Image.fromarray(self.cv2img)
        crop_image = ImageTk.PhotoImage(crop_image)
        self.panel.configure(image = crop_image)
        self.panel.image = crop_image

        
    def exitProgram(self):
        os._exit(0)

if __name__ == '__main__':

    root=Tk()
    ph=ImageProcessor(root)
    root.geometry("900x600")
    root.mainloop()
