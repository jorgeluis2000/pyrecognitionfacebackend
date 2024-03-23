from decouple import config

COM_SERIAL: str = config("COM_SERIAL")
BAUD_SERIAL: int = config("BAUD_SERIAL")