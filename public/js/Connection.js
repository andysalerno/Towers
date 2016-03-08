// setup websocket with callbacks
var ws = new WebSocket('ws://localhost:9000/');
ws.onopen = function() {
    console.log('CONNECT');
    ws.send("I'm the client!")
};

ws.onclose = function() {
    console.log('DISCONNECT');
};

ws.onmessage = function(event) {
    console.log('MESSAGE: ' + event.data);

    msg = safeParseJSON(event.data);
    if (msg && msg.hasOwnProperty('type')) {
        if (msg.type == 'chat') {
            if(chatbox) {
                chatbox.addMsg(msg.id, msg.msg);
            }
        }
    }
};

ws.sendChat = function(id, msg) {
    ws.send(JSON.stringify({
        type: "chat",
        id: id,
        msg: msg
    }));
}

ws.towerRequest = function(id, msg) {
    ws.send(JSON.stringify({
        type: "towerRequest",
        id: id,
        msg: msg
    }));
}

ws.creepRequest = function(id, msg) {
    ws.send(JSON.stringify({
        type: "creepRequest",
        id: id,
        msg: msg
    }));
}

var userID = 0; // Placeholder