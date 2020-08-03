from flask import Flask
from flask_socketio import SocketIO, join_room, send, emit
#from os import path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/")
def helloWorld():
    return "Hello World"

@socketio.on("join")
def when_join(data):
    """
    If the client intentions are to connect therefore
    :param data: that data coming from the client willing to connect.
    A dict {"password":"id"}
    :return: None, a boolean method but does what's necessarily for the connection.
    """
    username = data['password']
    if username == "vany":
        room = "Room01"
        join_room(room)
        send(username + ' has entered the room.', room=room, broadcast=True)
    room = "Kitchen"
    join_room(room)
    send(username + ' has entered the room.', room=room, broadcast=True)

@socketio.on('station')
def stationData(data):
    """
    This event is when a station sends in data
    :param data:
    :return:
    """
    #emit(data["id"] + ' has sent : '+ data["data"], room=data["room"], broadcast=True)
    print(data)

if __name__ == '__main__':
    socketio.run(app, debug=True)