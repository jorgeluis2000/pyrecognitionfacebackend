import cv2
import numpy as np
import imutils


class RecognitionColor:
    
    def __init__(self, border_color = (0, 255, 0), activate_pos = True, activate_circule_medium = True, activate_contours = True, contours_color = (38, 255, 255), area = 500) -> None:
        self.__borderColor = border_color
        self.__contoursColor = contours_color
        self.__area = area
        self.__activePos = activate_pos
        self.__activateCirculeMedium = activate_circule_medium
        self.__activate_contours = activate_contours
        
    def changeBorderColor(self, border_color: tuple):
        self.__borderColor = border_color
    
    def changeArea(self, new_area: int):
        self.__area = new_area
    
    def detectColorObject(self, mask: np.ndarray, frame: np.ndarray):
        contorno = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contorno = imutils.grab_contours(contorno)
        for c in contorno:
            area = cv2.contourArea(c)
            if area > self.__area:
                if self.__activate_contours is True:
                    cv2.drawContours(frame, [c], -1, self.__contoursColor, 3)
                M = cv2.moments(c)
                # if M['m00'] == 0:
                #   M['m00'] = 1
                cx = int(M['m10'] / M['m00'])        
                cy = int(M['m01'] / M['m00'])
                if self.__activateCirculeMedium is True:
                    cv2.circle(frame, (cx, cy), 7, self.__borderColor, -1)
                if self.__activePos is True:
                    cv2.putText(frame, f'x: {cx}, y: {cy}', (cx-20, cy-20), cv2.FONT_ITALIC, 0.6, self.__borderColor, 2)