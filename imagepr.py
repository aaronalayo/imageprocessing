import cv2
import PIL

class ImageProcessor:
    filename = filedialog.askopenfilename(title='open')
    img = cv2.imread(filename)
 
    cv2.imshow('sample image',img)
 
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys the window showing image