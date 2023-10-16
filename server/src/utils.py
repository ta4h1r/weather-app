from datetime import datetime
from constants import ERR_CODES

def printTime():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("\n" + dt_string)