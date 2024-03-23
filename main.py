
from io import StringIO
from contextlib import redirect_stdout
from src.config.server.Server import Server
from src.config.frontend.WebView import WebView

if __name__ == "__main__":
    stream = StringIO()
    server = Server()
    # serverIO = ServerIO(server.getApp())
    with redirect_stdout(stream):
        windows = WebView(server=server.getApp())
        windows.start()
    