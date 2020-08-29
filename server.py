from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, send, disconnect, emit
from flask_sqlalchemy import SQLAlchemy
import os, json
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

@app.route("/")
def helloWorld():
    """
    Returns a page stating 'Welcome to the server.'
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
    if "password" in data.keys() and "room" not in data.keys(): #If it's a client
        password = data['password']
        user_object = findClient(password)
        if user_object: #Meaning the user exists in the database
            dict = initiationDataForApp(user_object)
            emit("initial", dict)
        else:
            disconnect() #Disconnect the user if he is not recognised

    elif "station" in data.keys(): #If it's a station
        username = data['station']
        room = findRoomForStation(username)
        if room:
            join_room(room)
            emit("initial", {"room":room})
        else:
            disconnect() #Disconnect the user if he is not recognised

    elif "room" in data.keys() and "password" in data.keys(): #If it's a Room Tab
        password = data['password']
        user_object = findClient(password)
        if data["room"] in user_object.rooms :
            dict = initiationDataForRoomTab(data["room"])
            emit("initial", dict)
        else:
            disconnect()

    else: #Unkown protocol
        disconnect()


@socketio.on('data')
def stationData(data):
    """
    This event is when a station sends in data
    :param data: data received from the stations.
    :return: None
    """
    emit("data", data, room=data["room"])


def findRoomForStation(stationId):
    """
    This functions return the string of the room that's in the database
    :param stationId: a string, which is the stationId
    :return a string, else None
    """
    try:
        room_objects = models.Room.query.all()
        for room in room_objects:
            if stationId in room.stations:
                return room.id
        return

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
        # Checks if the room exists
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
        station_object = models.Station.query.filter_by(id=stationId).first()
        return station_object

    except Exception as e:
        print(e)


def initiationDataForApp(user_object):
    """
    The function loads up all the initial data to send back to the App.
    :param user_object: A model object containing his row in the user database table
    :return: a dict, containing all the infos.
    """
    dict = {"admin": 1 if user_object.admin else 0}
    rooms = []

    for roomId in user_object.rooms:
        room_object = findRoom(roomId)
        if room_object:
            join_room(roomId)  # Adds the socket in a room
            room_dict = {"id": roomId}
            stations_list = []

            for stationId in room_object.stations:
                station_object = findStation(stationId)
                if station_object:
                    station_dict = {"id": str(stationId),
                                    "sensors": station_object.sensors}
                    stations_list.append(station_dict)

            room_dict["stations"] = stations_list
            rooms.append(room_dict)

    dict["rooms"] = rooms
    return dict


def initiationDataForRoomTab(roomId):
    """
    The function loads up all the initial data to send back to the App.
    :param user_object: a row in the user table, database.
    :param room: the string of the room id.
    :return: a dict, containing all the infos.
    """
    room_object = findRoom(roomId)
    if room_object:
        join_room(roomId)  # Adds the socket in a room
        room_dict = {"id": roomId}
        stations_list = []

        for stationId in room_object.stations:
            station_object = findStation(stationId)
            if station_object:
                station_dict = {"id": str(stationId),
                                "sensors": station_object.sensors}
                stations_list.append(station_dict)

        room_dict["stations"] = stations_list
    return room_dict


if __name__ == '__main__':
    socketio.run(app, debug=True)
