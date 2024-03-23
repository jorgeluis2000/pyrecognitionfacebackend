from tkinter import *
from PIL import Image, ImageTk
from ultralytics import YOLO
import matplotlib.pyplot as plt
import numpy as np
import cv2

model= YOLO("best.pt")

def capturedImage():
    cameraObject = cv2.VideoCapture(0)
    if cameraObject is not None:
        #Captura frame-by-frame
        ret, frame = cameraObject.read()
        if ret == True:
            # Implementación del modelo
            resultados = model.predict(frame, imgsz = 640)
            print("resultados: \n" + str(resultados[0]))
            print("\n\n\nCajas: \n" + str(resultados[0].boxes))
            print("\n\n\nCajas: \n" + str(resultados[0].boxes.cls))
            
            anotaciones = resultados[0].plot()
            # Transformar array to image
            img = Image.fromarray(anotaciones)
            
            img = img.resize((440, 280))
            imgTk = ImageTk.PhotoImage(image=img)
            captureLabel.config(image=imgTk)
            captureLabel.image = imgTk
            # Mostrar frame
            plt.imshow(anotaciones)
            plt.title('Image campture')
            plt.show()
        else:
            captureLabel.image = ""
            cameraObject.release()
    cameraObject.release()

def closeMyWindow():
    raiz.destroy()

#Cuando todo este hecho cierra el programa



raiz = Tk()
raiz.geometry("640x580")
raiz.title("Capture recognition")

mainFrame = Frame()
mainFrame.config(width = "640", height = "480")
mainFrame.place(x = 0, y = 0)
# Frames
btnFrame = Frame()
btnFrame.config(width = "640", height = "100")
btnFrame.place(x = 0, y = 480)

labelFrame = Frame()
labelFrame.config(width = "100", height = "300")
labelFrame.place(x = 500, y = 50)

captureLabel = Label(mainFrame)
captureLabel.place(x = 0, y=0)


# Botones
btnCapture = Button(btnFrame, text="Capturar Imagen", command=capturedImage)
btnCapture.place(x=20, y=40)

btnCerrar = Button(btnFrame, text="Cerrar", command=closeMyWindow)
btnCerrar.place(x=510, y=40)

# Labels

labelShowPos = Label(labelFrame, text="Mi posición")
labelShowPos.place(x=5, y=5)

raiz.mainloop()