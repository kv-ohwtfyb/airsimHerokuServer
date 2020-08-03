let io = require('socket.io-client'); //Imports the library
socket = io.connect("http://127.0.0.1:5000"); //Connects to the server
const data = {
    "password":"vany"
}

socket.on('connect', function () { //When connected
    console.log("socket connected");
    socket.emit("join", data) //This kinda shows the intention of the user with his/her details.
});

socket.on('message',function (message){
    console.log(message)
});