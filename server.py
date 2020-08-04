from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, send, emit
import os
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

messages = [] #It's a list containing the activities that happened on the server

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, '/database/dbTesting.sqlite')

@app.route("/")
def helloWorld():
    """
    Returns a page containing all the activities that went on since the last launch of the server
    """
    return render_template("index.html", messages=messages)

@socketio.on("join")
def when_join(data):
    """
    If the client intentions are to connect therefore
    :param data: that data coming from the client willing to connect.
    A dict {"password":"id"}
    :return: None, a boolean method but does what's necessarily for the connection.
    """
    try: #if it's a client
        username = data['password']
        rooms = findRoomForClient(username)
        if rooms:
            for room in rooms:
                join_room(room)
                send(username + ' has entered the ' + room, room=room, broadcast=True)
                messages.append(username + ' has entered the ' + room)

    except: #if it's a station
        username = data['id']
        room = findRoomForStation(username)
        if room:
            messages.append(username + ' has entered the ' + room)
            join_room(room)
            send(username + ' has entered the' + room , room=room, broadcast=True)

@socketio.on('station')
def stationData(data):
    """
    This event is when a station sends in data
    :param data:
    :return:
    """
    room = findRoomForStation(data["id"])
    send(data["id"] + ' has sent : '+ data["data"], room=findRoomForStation(data["id"]), broadcast=True)
    messages.append(data["id"] + ' has sent : '+ data["data"] + "to the" + room )

def findRoomForStation(stationId):
    """
    This functions return the string of the room that's in the database
    :param stationId: a string, which is the stationId
    :return a string, else None
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT roomId FROM rooms WHERE stations=(?)",(stationId,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        messages.append(str(e))

def findRoomForClient(password):
    """
    This functions returns the tuple of the rooms that client has acces to
    in the database
    :param tuple: a string, which is the password
    :return a tuple, else None
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT(rooms) FROM users WHERE password=(?)",(password,))
        result = cursor.fetchone()
        conn.close()
        return result
    except Exception as e:
        messages.append(str(e))

if __name__ == '__main__':
    socketio.run(app, debug=True)