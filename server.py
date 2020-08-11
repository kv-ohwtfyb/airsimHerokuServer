from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, send, disconnect, emit
from flask_sqlalchemy import SQLAlchemy
import os, sqlite3
import models

#Configure App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#Configure database
#The next line is when we are testing locally
#app.config["SQLALCHEMY_DATABASE_URI"]="""postgres://mynykzmxrgomnr:37d166bbca8361ae9bff92d8814e534458776511f96498f9246714161dbc3439@ec2-54-247-118-139.eu-west-1.compute.amazonaws.com:5432/ddvcl8up8gjd8l"""
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") #This is for security mesures

db = SQLAlchemy(app)

#Variables
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, '/database/dbTesting.sqlite')

@app.route("/")
def helloWorld():
    """
    Returns a page containing all the activities that went on since the last launch of the server
    """
    return render_template("index.html")

@socketio.on("join")
def when_join(data):
    """
    If the client intentions are to connect therefore
    :param data: that data coming from the client willing to connect.
    A dict {"password":"id"}
    :return: None, a boolean method but does what's necessarily for the connection.
    """
    if "password" in data.keys(): #if it's a client
        password = data['password']
        user_object = findClient(password)
        if user_object:
            dict = {"admin":1 if user_object.admin else 0}
            rooms = []

            for roomId in user_object.rooms:
                room_object = findRoom(roomId)
                if room_object:
                    join_room(roomId) #Adds the user in a room
                    room_dict = {"id":roomId}
                    stations_list = []

                    for stationId in room_object.stations:
                        station_object = findStation(stationId)
                        if station_object:
                            station_dict = {"id":str(stationId),
                                            "sensors": station_object.sensors}
                            stations_list.append(station_dict)

                    room_dict["stations"] = stations_list
                    rooms.append(room_dict)

            dict["rooms"]=rooms
            send("sending")
            emit("initial", dict)
        else:
            disconnect() #Disconnect the user if he is not recognised


    elif "station" in data.keys(): #if it's a station
        username = data['station']
        room = findRoomForStation(username)
        if room:
            join_room(room)
            send(username + ' has entered the' + room , room=room, broadcast=True)
    elif "room" in data.keys(): #If it's a Room Tab
        pass

    else: #Unkown protocol
        disconnect()

@socketio.on('station')
def stationData(data):
    """
    This event is when a station sends in data
    :param data:
    :return:
    """
    room = findRoomForStation(data["id"])
    send(data["id"] + ' has sent : '+ data["data"], room=findRoomForStation(data["id"]), broadcast=True)

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
        print(e)

def findClient(password):
    """
    This functions returns the tuple of the rooms that client has acces to
    in the database
    :param tuple: a string, which is the password
    :return a tuple, else None
    """
    try:
        # Checks if the user exists
        user_object = models.User.query.filter_by(password=password).first()
        return user_object

    except Exception as e:
        print(e)

def findRoom(roomId):
    """
    This function returns a Room Custom db SQAlchemy model for a room if it's
    in the database.
    :param roomId: the room name, Id.
    :return: Room model if it exists else None.
    """
    try:
        # Checks if the user exists
        room_object = models.Room.query.filter_by(id=roomId).first()
        return room_object

    except Exception as e:
        print(e)

def findStation(stationId):
    """
    This function returns a Station Custom db SQAlchemy model for a room if it's
    in the database.
    :param stationId: the station name, Id.
    :return: Station model if it exists else None.
    """
    try:
        # Checks if the user exists
        room_object = models.Station.query.filter_by(id=stationId).first()
        return room_object

    except Exception as e:
        print(e)

if __name__ == '__main__':
    socketio.run(app, debug=True)