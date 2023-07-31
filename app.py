import socketio
from flask import Flask

app = Flask(__name__, server_name="localhost", server_port=8080)
sio = socketio.Server(app)

rooms = {}

@app.route("/")
def index():
    return render_template("index.html")

@sio.on("connect")
def connect(sid):
    print("Client connected: " + sid)

    room = sid
    if room not in rooms:
        rooms[room] = []

@sio.on("message")
def message(sid, message):
    print("Received message from " + sid + ": " + message)

    data = json.loads(message)
    name = data["name"]
    room = data["room"]
    message = data["message"]

    messages = rooms[room]
    messages.append((name, message))

    sio.emit("message", {"name": name, "room": room, "messages": messages}, room=room)

@sio.on("disconnect")
def disconnect(sid):
    print("Client disconnected: " + sid)

    room = sid
    del rooms[room]

if __name__ == "__main__":
    app.run()
