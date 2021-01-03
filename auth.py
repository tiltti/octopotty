import websocket, json, requests
import configparser

try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_open(ws):
    auth_message = "{ \"auth\": \""+config['auth']['octopi.username']+":"+session+"\" }"
    print("Sending auth message: {}".format(auth_message))
    ws.send(auth_message)

def on_message(ws, message):
    print("Incoming message: ")
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("Closing Socket...")

def read_config(configfile):
    print("Reading configuration...")
    config.read(configfile)
    print("Username: {}".format(config['auth']['octopi.username']))
    print("Password: {}".format(config['auth']['octopi.password'])) 
    print("Hostname: {}".format(config['auth']['octopi.hostname']))

if __name__ == "__main__":
    config = configparser.ConfigParser()
    read_config("octopotty.ini")
    logindata = { 'user': config['auth']['octopi.username'], 'pass': config['auth']['octopi.password'] }
    r = requests.post("http://"+config['auth']['octopi.hostname']+"/api/login", json=logindata, verify=False)
    #print('{} {} '.format(r.status_code, r.json()))
    data = r.json()
    print('session: {}'.format(data['session']))
    session = data['session']
    ws_host = "ws://"+config['auth']['octopi.hostname']+"/sockjs/websocket"
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(ws_host,
        on_open = on_open,
        on_message = on_message,
        on_error = on_error,
        on_close = on_close)
    ws.run_forever()
