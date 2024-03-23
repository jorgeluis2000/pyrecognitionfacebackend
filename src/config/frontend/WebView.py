import webview
from src.utils.constants.ServerConstants import PORT_DEFAULT
class WebView:
    
    def __init__(self, server) -> None:
        self.mywindow = webview.create_window('Hello world', server, min_size=(800, 600), http_port=PORT_DEFAULT, resizable=True,js_api=[
            'navigator.mediaDevices.getUserMedia({ video: true })'
        ])
        
    
    def start(self):
        webview.start(debug=False)