import websocket
import json
import threading
import os
import ctypes
from playsound import playsound
from plyer import notification
NoW = False

def EEWsound(language):
    if language == 'English':
        playsound('sounds/Shaking(EN).mp3')
    elif language == 'Japanese':
        playsound('sounds/Shaking(JP).mp3')
    elif language == 'Chinese':
        playsound('sounds/Shaking(CH).mp3')
    elif language == 'Spanish':
        playsound('sounds/Shaking(ES).mp3')
    elif language == 'Korean':
        playsound('sounds/Shaking(SK).mp3')
    elif language == 'Polish':
        playsound('sounds/Shaking(PL).mp3')
    playsound('sounds/Emergency_Alert02-1.mp3')
    #playsound('sounds/Emergency_Alert01-1.mp3')
    notification.notify(
        title="EARTHQUAKE ALERT!",
        message="drop cover and hold on",
        app_icon='images/drop.ico',  # Path to a custom icon file (.ico). Set to None for no icon.
        timeout=5  # Duration in seconds
    )

class jmaEEW:
    global EEWsound
    def __init__(self, data, language):
        self.data = data
        self.language = language
    def displayAlert(self):
        if self.data.get("isFinal"):
            print("THIS IS THE FINAL REPORT")
        print("Earthquake Alert! (JAPAN EEW)")
        print(f"Title: {self.data.get('Title')}")
        print(f"Location: {self.data.get('Hypocenter')}")
        print(f"Magnitude: {self.data.get('Magunitude')}")
        print(f"Max Intensity: {self.data.get('MaxIntensity')}")
        print(f"Maximum earthquake intensity: {self.data.get('WarnArea').get('Shindo1')}")
        print(f"Origin time: {self.data.get('OriginTime')}")
        print(f"Announced time: {self.data.get('AnnouncedTime')}")
        print(f"Depth: {self.data.get('Depth')}")
        print(f"Warning area arrival: {self.data.get('WarnArea').get('Arrive')}")
        print(f"Warning Areas: {self.data.get('WarnArea').get('Chiiki')}")
        print(f"Method: {self.data.get('isAssumption')}")
        if self.data.get("isCancel"):
            for i in range(5):
                print('FALSE EEW ALARM')
        EEWsound(self.language)
class cwaEEW:
    global EEWsound
    def __init__(self, data, language):
        self.data = data
        self.language = language
    def displayAlert(self):
        print("Earthquake Alert! (CWA EEW)")
        print(f"Magnitude: {self.data.get('Magunitude')}")
        print(f"ID: {self.data.get('ID')}")
        print(f"Depth: {self.data.get('Depth')}")
        print(f"Time: {self.data.get('OrginTime')}")
        print(f"Location: {self.data.get('HypoCenter')}")
        print(f"Maximum intensity: {self.data.get('MaxIntensity')}")
        EEWsound(self.language)

class scEEW:
    global EEWsound
    def __init__(self, data, language):
        self.data = data
        self.language = language
    def displayAlert(self):
        print("Earthquake Alert! (SC EEW)")
        print(f"Magnitude: {self.data.get('Magunitude')}")
        print(f"ID: {self.data.get('ID')}")
        print(f"Depth: {self.data.get('Depth')}")
        print(f"Time: {self.data.get('OrginTime')}")
        print(f"Location: {self.data.get('hypoCenter')}")
        print(f"Maximum intensity: {self.data.get('MaxIntensity')}")
        EEWsound(self.language)

class fjEEW:
    global EEWsound
    def __init__(self, data, language):
        self.data = data
        self.language = language
    def displayAlert(self):
        print("Earthquake Alert! (FJ EEW)")
        print(f"Magnitude: {self.data.get('Magunitude')}")
        print(f"ID: {self.data.get('ID')}")
        print(f"Depth: {self.data.get('Depth')}")
        print(f"Time: {self.data.get('OrginTime')}")
        print(f"Location: {self.data.get('HypoCenter')}")
        print(f"Maximum intensity: {self.data.get('maxIntensity')}")
        print(f"ReportTIme: {self.data.get('ReportTime')}")
        print(f"Final: {self.data.get('isFinal')}")
        EEWsound(self.language)

class cencEqList:
    global EEWsound
    def __init__(self, data, language):
        self.data = data
        self.language = language
    def displayAlert(self):
        print("Earthquake Alert! (CENC EQLIST)")
        for key, report in self.ata.items():
            if key.startswith('No'):  
                print(f"Earthquake Report {key}:")
                print(f"Magnitude: {self.report.get('magnitude')}")
                print(f"Depth: {self.report.get('depth')}")
                print(f"Time: {self.report.get('time')}")
                print(f"Location: {self.report.get('location')}")
                EEWsound(self.language)
                NoW = False
class noEEW:
    global EEWsound
    def __init__(self):
        pass
    def noAlert(self):
        print("No EEW issued")
        notification.notify(
        title="NO EEW ISSUED",
        message=" ",
        app_icon='images/Sesnaquake3.ico',  # Path to a custom icon file (.ico). Set to None for no icon.
        timeout=2  # Duration in seconds
        )
        

def on_message(ws, message):
    global NoW
    language = 'Chinese'
    data = json.loads(message)
    if data.get("type") == "jma_eew":
        alert = jmaEEW(data, language)
        alert.displayAlert()
        NoW = False
    elif data.get("type") == "cwa_eew":
        alert = cwaEEW(data, language)
        alert.displayAlert()
        NoW = False
    elif data.get("type") == "sc_eew":
        alert = scEEW(data, language)
        alert.displayAlert()
        NoW = False
    elif data.get("type") == "fj_eew":
        alert = fjEEW(data, language)
        alert.displayAlert()
        NoW = False
    elif data.get("type") == "cenc_eqlist":
        alert = cencEqList(data, language)
        alert.displayAlert()
        NoW = False
    elif NoW == False:
        alert = noEEW()
        alert.noAlert()
        NoW = True

# Function for handling errors
def on_error(ws, error):
    print("Error:", error)

# Function for handling the closure of the connection
def on_close(ws, close_status_code, close_msg):
    print("Connection closed.")

# Function to execute when the connection is opened (DELETED FOR NOW)
def on_open(ws):
    global NoW
    print("WebSocket connection established.")

# Function to run a WebSocket connection in a separate thread
def run_websocket(ws_url):
    ws = websocket.WebSocketApp(ws_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    #ws.on_open = on_open
    ws.run_forever()

# Dictionary to map the different data sources to their respective WebSocket URLs
ws_urls = {
    "jma_eew": "wss://ws-api.wolfx.jp/jma_eew",
    "cenc_eqlist": "wss://ws-api.wolfx.jp/cenc_eqlist",
    "cwa_eew": "wss://ws-api.wolfx.jp/cwa_eew",
    "sc_eew": "wss://ws-api.wolfx.jp/sc_eew",
    "fj_eew": "wss://ws-api.wolfx.jp/fj_eew"
}

# Create and start a separate thread for each WebSocket URL
threads = []
for source, url in ws_urls.items():
    thread = threading.Thread(target=run_websocket, args=(url,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()
