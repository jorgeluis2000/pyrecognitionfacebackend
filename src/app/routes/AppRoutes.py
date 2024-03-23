import ast
from src.app.services.Camera import Camera
from flask import Flask, render_template, Response, jsonify, request, json
from src.utils.function.ColorTransform import hex_to_rgb, rgbToHsv, rgbToBgr

class AppRoutes:

    def __init__(self, app: Flask, myCamera: Camera) -> None:
        self.app = app
        self.__my_camera = myCamera
        self.router()

    def change_camera(self, index_camera: int):
        self.__my_camera.destroy_camera()
        new_camera = Camera(index_camera=index_camera)
        if new_camera.cameraStatus:
            self.__my_camera = new_camera
            return True
        self.__my_camera.recreate()
        return False

    def router(self):

        @self.app.after_request
        def add_header(response: Response) -> Response:
            response.headers['Cache-Control'] = 'no-store'
            return response

        @self.app.route('/api/wave/<string:name>')
        def wave_someone(name) -> Response:
            return jsonify({
                "ok": True,
                "message": f'Hola {name}'
            })

        @self.app.route('/api/wave')
        def get_wave() -> Response:
            return jsonify({
                "ok": True,
                "message": "Hola mundo!!"
            })
        
        @self.app.route('/mask_feed')
        def mask_feed() -> Response:
            return Response(self.__my_camera.getGenerateMask(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.app.route('/result_recognition')
        def result_recognition() -> Response:
            try:
                result = ast.literal_eval(str(self.__my_camera.getResult()).replace('tensor(', '[').replace(')', ']'))
                names = ast.literal_eval(str(self.__my_camera.getNames()))
                
                return jsonify({
                    "ok": True,
                    "http_code": 2000,
                    "message": "Estos son los resultados.",
                    "data": json.loads(json.dumps({
                        "result": result,
                        "names": names
                    }))
                })
            except Exception as e:
                print('❌ System Error on AppRouter ~ result_recognition():' + str(e))
                return jsonify({
                    "ok": False,
                    "http_code": 4000,
                    "message": "Tenemos problemas en nuestros servicios ahora mismo.",
                    "data": json.loads(json.dumps({
                        "result": [],
                        "names": {}
                    }))
                })

        @self.app.route('/capture_recognition')
        def capture_recognition():
            return Response(self.__my_camera.get_capture_moment(), mimetype='multipart/x-mixed-replace; boundary=frame')


        @self.app.route('/video_feed')
        def video_feed():
            return Response(self.__my_camera.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.app.route('/video_option/<int:index_camera>')
        def change_camera(index_camera):
            changeCamera = self.change_camera(index_camera=index_camera)
            if not changeCamera:
                return jsonify({
                    "ok": False,
                    "message": "La camara no se pudo cambiar."
                })
            return jsonify({
                "ok": True,
                "message": "La camara se ha cambiado.",
                "data": changeCamera
            })

        @self.app.route('/')
        def pagina():
            return render_template('index.html')
        
        @self.app.route('/current_color', methods=['POST'])
        def current_color():
            try:
                option: str = request.json['option']
                currentColorHSV = None
                currentColor = None
                if option == 'light':
                    currentColor = self.__my_camera.getColorLight().getColorHex()
                    currentColorHSV = self.__my_camera.getColorLight().getColorHSV()
                elif option == 'dark':
                    currentColor = self.__my_camera.getColorDark().getColorHex()
                    currentColorHSV = self.__my_camera.getColorDark().getColorHSV()
                else:
                    return jsonify({
                        "ok": False,
                        "message": "La opción es invalida."
                    })
                return jsonify({
                    "ok": True,
                    "message": f'¡Este es el color {option} actual!',
                    "color": f'{currentColor}',
                    "color_hsv": f'{currentColorHSV}'
                })
            except Exception as e:
                return jsonify({
                    "ok": False,
                    "message": "¡No se pudo obtener el color!",
                    "error": f'{e}'
                })
        
        @self.app.route('/change_color', methods=['POST'])
        def change_color():
            try:
                option: str = request.json['option']
                color: str = request.json['color']
                newColor = None
                newColorHSV = None
                
                if option == 'light':
                    rgbColor = hex_to_rgb(color)
                    bgrColor = rgbToBgr(rgbColor)
                    newColor = rgbToHsv(bgrColor)
                    self.__my_camera.changeColorLight(h=newColor[0], s=newColor[1], v=newColor[2])
                    newColor = self.__my_camera.getColorLight().getColorHex()
                    newColorHSV = self.__my_camera.getColorLight().getColorHSV()
                elif option == 'dark':
                    rgbColor = hex_to_rgb(color)
                    bgrColor = rgbToBgr(rgbColor)
                    newColor = rgbToHsv(bgrColor)
                    self.__my_camera.changeColorDark(h=newColor[0], s=newColor[1], v=newColor[2])
                    newColor = self.__my_camera.getColorDark().getColorHex()
                    newColorHSV = self.__my_camera.getColorDark().getColorHSV()
                else:
                    return jsonify({
                        "ok": False,
                        "message": "La opción es invalida."
                    })
                return jsonify({
                    "ok": True,
                    "message": "¡Se ha relizado el cambio de color!",
                    "color": f'{newColor}',
                    "color_hsv": f'{newColorHSV}'
                })
            except Exception as e:
                return jsonify({
                    "ok": False,
                    "message": "¡No se pudo realizar el cambio de color!",
                    "error": f'{e}'
                })
            

