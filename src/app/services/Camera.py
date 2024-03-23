import cv2
import os
from ultralytics import YOLO
from PIL import Image
import numpy as np
from src.app.services.RecognitionColor import RecognitionColor
from src.app.services.Color import Color


class Camera:
    
    def __init__(self, index_camera: int):
        ruta_actual = os.path.abspath(os.getcwd())
        self.__model= YOLO(os.path.join(ruta_actual, 'best.pt'))
        self.__names = {}
        self.__result = []
        self.__currentCamera = index_camera
        self.__camera = cv2.VideoCapture(index_camera)
        self.cameraStatus = self.statusCamera(index_camera)
        self.__colorLight = Color(0, 130, 130)
        self.__colorDark = Color(16, 255, 255)
        self.__rc = RecognitionColor()
        self.__frame = None
        self.__mask = None
    
    
    def getColorDark(self):
        return self.__colorDark
    
    def getColorLight(self):
        return self.__colorLight
    
    def getNames(self):
        return self.__names
    
    def getResult(self):
        return self.__result
    
    def statusCamera(self, index_camera: int):
        try:
            cap = cv2.VideoCapture(index_camera)
            if not cap.isOpened():
                return False
        except Exception as e:
            return False
        return True
    
    def changeColorLight(self, h: int, s: int,v: int):
        self.__colorLight.changeColorHSV(h, s, v)
        # self.__colorLight = Color(h, s, v)
        
    def changeColorDark(self, h: int, s: int,v: int):
        self.__colorDark.changeColorHSV(h, s, v)
        # self.__colorDark = Color(h, s, v)
    
    def destroy_camera(self):
        self.statusCamera = False
        self.__camera.release()
    
    def recreate(self):
        self.statusCamera = True
        self.__camera = cv2.VideoCapture(self.__currentCamera)
    
    def getFrame(self):
        return self.__frame
    
    def getMask(self):
        return self.__mask
    
    def getGenerateMask(self):
        try:
            _, buffer = cv2.imencode('.jpg', self.__mask)
            maskBuffer = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + maskBuffer + b'\r\n')
        except Exception as e:
            self.getGenerateMask()
        
        
    def get_capture_moment(self):
        try:
            resultados = self.__model.predict(self.__frame, imgsz = 640)
            self.__names = resultados[0].names
            self.__result = resultados[0].boxes.cls
            
            anotaciones = resultados[0].plot()
            self.__mask = anotaciones
            _, buffer = cv2.imencode('.jpg', self.__mask)
            frameBuffer = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frameBuffer + b'\r\n')
        except Exception as e:
            print('❌ System Error on Camera ~ getCaptureMoment', str(e))
            self.get_capture_moment()
    
    def generate_frames(self):
        try:
            while self.cameraStatus:
                success, self.__frame = self.__camera.read()
                if not success:
                    break
                else:
                    _, buffer = cv2.imencode('.jpg', self.__frame)
                    frameBuffer = buffer.tobytes()
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frameBuffer + b'\r\n')
        except Exception as e:
            print('❌ System Error on Camera ~ generate_frames', str(e))
            self.generate_frames()
    