import os
import time as tm
from datetime import datetime

def dtime(file):
    return datetime.fromtimestamp(os.path.getmtime(file)).strftime("%Y-%m-%d, %A, %H:%M:%S")