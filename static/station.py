import socketio, random
from time import sleep

stationId = "staTion1AB"
sio = socketio.Client()
global joined
joined = False

def join():
    """
    When asking to join a room in the server
    :return:None
    """
    global joined
    sio.emit("join", {"id":stationId})
    joined = True

def connect():
    """
    Connects the socket to the url.
    :return: None
    """
    try:
        sio.connect("wss://kingvany.pythonanywhere.com:8845")
        print("CONNECTION ESTABLISHED")
        join()
    except Exception as e:
        print(e)
        print("ERROR WHEN CONNECTING TO THE SERVER")

@sio.on("disconnect")
def disconnect():
    """
    This function is when the socket gets disconnected
    :return: None
    """
    global joined
    joined = False
    print("CONNECTION FAILED")
    connect()

if __name__ == "__main__":
    connect()
    while joined:
        print(joined)
        sleep(10)
        sio.emit("station", {"data":str(random.randrange(0,100))})