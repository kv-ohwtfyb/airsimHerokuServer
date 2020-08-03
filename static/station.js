let io = require('socket.io-client'); //Imports the library
socket = io.connect("http://127.0.0.1:5000"); //Connects to the server


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

socket.on('connect',async function () { //When connected
    console.log("socket connected");
    socket.emit("join", {"password":"station1", "room":"Room01"}); //This kinda shows the intention of the user with his/her details.

    while (socket.connected) {
        await sleep(4000)
        socket.emit("station", {"password":"station1", "room":"Kitchen","data":String(Math.ceil(Math.random()*100))})
        console.log("sent")
    }
});

socket.on('message',function (message){
    console.log(message)
});

socket.on('disconnect', function () {
    console.log("t")
})