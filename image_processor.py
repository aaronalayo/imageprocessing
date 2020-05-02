import tkinter as tk
from tkinter import Frame, Tk, BOTH, Text, Menu, END, filedialog, Label
from PIL import ImageTk, Image
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
        fileMenu.add_command(label="Save")

               

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)
    
    def openfn(self):
        filename = filedialog.askopenfilename(title='open')
        return filename

    def open_img(self):
        x = self.openfn()
        img = Image.open(x)
        img = img.resize((500, 500), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = Label(root, image=img)
        panel.image = img
        panel.pack(fill=BOTH, expand=True)
        panel.place(x = 0, y= 0)
        
        

        return x
 

    
        
    def exitProgram(self):
        os._exit(0)

if __name__ == '__main__':

    root=Tk()
    ph=ImageProcessor(root)
    root.geometry("500x500+200+500")
    root.mainloop()
