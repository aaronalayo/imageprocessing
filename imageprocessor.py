import tkinter as tk
import cv2
from tkinter import Frame, Tk, BOTH, Text, Menu, END, filedialog, Label, Button, Entry
from PIL import ImageTk, Image
import numpy as np
import os
import filters




class ImageProcessor(Frame):
    """Image processor app 
    features: Open, Save, Quit, Undo, Add filters, Manipulate Image, Face detection 
    Arguments:
        Frame {[Tkinter]} -- [description]
    """

    def __init__(self, parent):
        Frame.__init__(self, parent)   

        self.parent = parent        
        self.initUI()
        
      
    def initUI(self):
        """Initiates the UI
        """
        self.parent.title("Image Processor")
        self.pack(fill=BOTH, expand=1)

        filebar = Menu(self.parent)
        self.parent.config(menu=filebar)
      
        fileMenu = Menu(filebar)
        filebar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Open", command=self.open_img)
        fileMenu.add_command(label="Save", command =self.save_img)
        fileMenu.add_command(label="Quit", command =self.exitProgram)

        editMenu = Menu(filebar)
        filebar.add_cascade(label= "Edit", menu= editMenu)
        editMenu.add_command(label="Undo", command = self.undo)
        editMenu.add_command(label="Redo", command = self.redo)

        imageMenu = Menu(filebar)
        filebar.add_cascade(label= "Image", menu= imageMenu)
        imageMenu.add_command(label= "Rotate Right", command= self.rotate_right_img)
        imageMenu.add_command(label= "Rotate Left", command= self.rotate_left_img)
        imageMenu.add_command(label= "Crop 4:3", command= self.crop_img)
        imageMenu.add_command(label= "Face detection", command= self.face_detect)

        filtersMenu = Menu(filebar)
        filebar.add_cascade(label= "Filters", menu= filtersMenu)
        filtersMenu.add_command(label= "Dither", command= self.call_filters_ditter)
        filtersMenu.add_command(label= "Gray Scale", command= self.call_convert_grayscale)
        filtersMenu.add_command(label= "Primary", command= self.call_convert_primary)

        filebar.add_cascade(label="Original image", command=self.show_original_img)

        self.btn = Button(root, text = 'Crop faces', command = self.crop_face)
        self.btn.pack_forget()

        self.panel = Label(root)
        self.panel.place(relx=.5, rely=.5, anchor="c")
        
        
        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)

        self.entry = Entry(root)
        self.entry.pack(side="right")
        self.b = Button(root,text='okay',command=self.increase_brightness)
        self.b.pack(side='right')

        self.states=[]
        self.states_redo=[] 

        self.drawing = False

    
    def undo(self):
        """Method to undo an action applied to an image
        It changes the image to its previous state which is saved in a list.
        """
        self.cv2img = self.states[-2]
        image = Image.fromarray(self.cv2img)
        image = ImageTk.PhotoImage(image)
        self.panel.configure(image = image)
        self.panel.image = image
        self.states_redo.append(self.states[-1])
        #del self.states[-1]
        self.states.pop()           

    def redo(self):
        self.cv2img = self.states_redo[-1]
        self.states.append(self.cv2img)
        image = Image.fromarray(self.cv2img)
        image = ImageTk.PhotoImage(image)
        self.panel.configure(image = image)
        self.panel.image = image
        #del self.states_redo[-1]
        self.states_redo.pop()

    def openfn(self):
        filename = filedialog.askopenfilename(title='open')
        return filename

   
    def open_img(self):
        """Opens an image and displays it on the panel
        It takes an image in OpenCV format, resizes it to fit the panel and converts it to 
        Pil Image and then displays it by configuring the panel 
        """
        self.cv2img = cv2.imread(self.openfn())
        self.cv2img = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2RGB)

        height_original = int(self.cv2img.shape[0])
        scale_percent = 500/height_original 
        width_new = int(self.cv2img.shape[1] * scale_percent)
        height_new = int(self.cv2img.shape[0] * scale_percent)
        dim = (width_new, height_new)
        self.cv2img = cv2.resize(self.cv2img,dim, interpolation = cv2.INTER_AREA)
        self.original = self.cv2img.copy()
        # Converts image from OpenCV to Pil Image
        image = Image.fromarray(self.cv2img)
        image = ImageTk.PhotoImage(image)
        self.panel.configure(image = image)
        self.panel.image = image

        #appends current image state to the list
        self.states.append(self.cv2img)
        
    
    def show_original_img(self):
        """Shows original image
        It changes the image to its first state
        """
        self.cv2img = self.original
        image = Image.fromarray(self.cv2img)
        image = ImageTk.PhotoImage(image)
        self.panel.configure(image = image)
        self.panel.image = image
        self.states.append(self.cv2img)

        
    
    def rotate_right_img(self):
        """Rotates the image 90 degrees clockwise
        """
        self.cv2img = cv2.rotate(self.cv2img, cv2.ROTATE_90_CLOCKWISE)
        rotated = Image.fromarray(self.cv2img)
        rotated = ImageTk.PhotoImage(rotated)
        self.panel.configure(image = rotated)
        self.panel.image = rotated
        self.states.append(self.cv2img)
        

    def rotate_left_img(self):
        """Rotates the image 90 degrees counterclockwise
        """
        self.cv2img = cv2.rotate(self.cv2img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        rotated = Image.fromarray(self.cv2img)
        rotated = ImageTk.PhotoImage(rotated)
        self.panel.configure(image = rotated)
        self.panel.image = rotated
        self.states.append(self.cv2img)

    def call_filters_ditter(self):
        """Calls the method convert_dithering in filters.py which returns a Pil dithered image
        """
        image = Image.fromarray(self.cv2img)
        im = filters.convert_dithering(image)
        img = ImageTk.PhotoImage(im)
        self.panel.configure(image = img)
        self.panel.image = img
        # # Convert RGB to BGR 
        self.cv2img = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        self.cv2img = self.cv2img[:, :, ::-1]
        self.states.append(self.cv2img)
        
    def call_convert_grayscale(self):
        """Calls the method convert_grayscale in filters.py which returns a Pil grayscaled image
        """
        image = Image.fromarray(self.cv2img)
        im = filters.convert_grayscale(image)
        img = ImageTk.PhotoImage(im)
        self.panel.configure(image = img)
        self.panel.image = img
        # # Convert RGB to BGR 
        self.cv2img = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        self.cv2img = self.cv2img[:, :, ::-1]
        self.states.append(self.cv2img)
        
    def call_convert_primary(self):
        """Calls the method convert_primary in filters.py 
        which returns a Pil image with only primary colors
        """
        image = Image.fromarray(self.cv2img)
        im = filters.convert_primary(image)
        img = ImageTk.PhotoImage(im)
        self.panel.configure(image = img)
        self.panel.image = img
        # # Convert RGB to BGR 
        self.cv2img = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        self.cv2img = self.cv2img[:, :, ::-1]
        self.states.append(self.cv2img)
        

    def save_img(self):
        """Saves the image in jpg to the hard drive
        """
        save_img = Image.fromarray(self.cv2img)
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if filename is None:
           return
        save_img.save(filename)
        
    def face_detect(self):
        """Detects faces on the image and creates a rectangle around each of them 
        """
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        self.gray = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2GRAY)
        self.cv2img = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2RGB)
       
        # create an array of the positions of each face 
        # and then iterates through it to draw a rectangle around all faces
        faces = self.face_cascade.detectMultiScale(self.gray, 1.3, 5)
        for (x, y, w, h) in faces:
            self.cv2img = cv2.rectangle(self.cv2img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        self.cv2img = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2RGB)
        faceimg = Image.fromarray(self.cv2img)
        faceimg = ImageTk.PhotoImage(faceimg)
        self.panel.configure(image = faceimg)
        self.panel.image = faceimg
        
        #makes the button for crop faces visible
        self.btn.pack(side = 'right')

        self.states.append(self.cv2img)
        
    def crop_face(self):
        """Crops every face from the image and displays it as a new photo 
        in a new window where it can be saved
        """
        faces = self.face_cascade.detectMultiScale(self.gray, 1.3, 5)
        self.cv2img = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2RGB)
        face_crop = []
        for f in faces:
            x, y, w, h = [ v for v in f ]
            
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
        self.btn.pack_forget()

            
    def crop_img(self):
        """Crops the image in 4:3 format
        """
        self.cv2img = self.cv2img[0:300, 0:400]
        crop_image = Image.fromarray(self.cv2img)
        crop_image = ImageTk.PhotoImage(crop_image)
        self.panel.configure(image = crop_image)
        self.panel.image = crop_image
        self.states.append(self.cv2img)

    
    def increase_brightness(self):
        value = int (self.entry.get())
        hsv = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value

        final_hsv = cv2.merge((h, s, v))
        self.cv2img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        
        bright_image = Image.fromarray(self.cv2img)
        bright_image = ImageTk.PhotoImage(bright_image)
        self.panel.configure(image = bright_image)
        self.panel.image = bright_image
        self.states.append(self.cv2img)
        
    def exitProgram(self):
        """Exits the program
        """
        os._exit(0)
        
        
if __name__ == '__main__':

    root=Tk()
    ph=ImageProcessor(root)
    root.geometry("1920x1060")
    root.mainloop()
