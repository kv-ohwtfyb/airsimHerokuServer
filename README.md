# AirSim (Real Time Data Monitor) Server

## Abstract
AirSim is a project about realtime data monitoring of temperature and humidity data comming from multiples Raspberry Pis.
This repository is connected to a Heroku Server that executes the pushed code here

## Server

This server is code in Python using Flask-SocketIo. The reason why is that *Flask-SocketIO gives Flask applications access to low latency bi-directional
communications between the clients and the server. The client-side application can use any of the SocketIO client libraries in Javascript, Python, C++, Java and Swift, or any other compatible client to establish a permanent connection to the server.*

## Clients 

### Monitor

There's another [repository](https://github.com/kv-ohwtfyb/airsim-StationGadgetGUI) that I used to implement the windows UI for data visualisation. It was written in QML and JavaScript.

### Sensors 

The sensor code is currently private for various reasons but will be soon available. In my case I used three Raspberry Pis.
