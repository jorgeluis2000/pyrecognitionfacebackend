import cv2
import numpy as np

def hsvToRgb(hsv_color: list[int]):
    hsvColor = np.array([[hsv_color]].copy(), np.uint8)
    rgb_color = cv2.cvtColor(hsvColor, cv2.COLOR_HSV2RGB)
    return list(rgb_color[0][0])

def rgb_to_hex(rgb: list[int]):
    # Validar que los valores RGB estén en el rango correcto (0-255)
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    if not (0 <= red <= 255) or not (0 <= green <= 255) or not (0 <= blue <= 255):
        raise ValueError("Los valores RGB deben estar en el rango de 0 a 255.")

    # Convertir los valores RGB a su representación hexadecimal
    hex_color = '#{:02x}{:02x}{:02x}'.format(red, green, blue)
    
    return hex_color

def hex_to_rgb(hex_color: str):
    # Validar que el valor hexadecimal tenga el formato adecuado
    if not isinstance(hex_color, str) or not hex_color.startswith("#") or len(hex_color) != 7:
        raise ValueError("El valor hexadecimal debe tener el formato '#RRGGBB'.")

    # Convertir el valor hexadecimal a los componentes RGB
    red = int(hex_color[1:3], 16)
    green = int(hex_color[3:5], 16)
    blue = int(hex_color[5:7], 16)

    return [red, green, blue]

def rgbToHsv(rgb_color: list[int]):
    rgbCalor = np.uint8([[rgb_color.copy()]])
    hsvColor = cv2.cvtColor(rgbCalor, cv2.COLOR_BGR2HSV)
    return list(hsvColor[0][0])

def rgbToBgr(color_rgb: list[int]):
    colorBgr = color_rgb[::-1]
    return colorBgr

def hex_to_hsv(hex_value):
    # Convertir el valor hexadecimal a RGB
    rgb = tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))

    # Convertir el valor RGB a HSV
    hsv = cv2.cvtColor(np.uint8([[rgb]]), cv2.COLOR_RGB2HSV)[0][0]

    return list(hsv)

def hsv_to_hex(hsv):
    # Convertir el valor HSV a RGB
    rgb = cv2.cvtColor(np.uint8([[hsv]]), cv2.COLOR_HSV2RGB)[0][0]

    # Convertir el valor RGB a hexadecimal
    hex_value = '#{:02x}{:02x}{:02x}'.format(*rgb)

    return hex_value