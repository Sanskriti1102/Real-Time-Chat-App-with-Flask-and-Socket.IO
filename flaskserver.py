from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder='static', static_url_path='')
socketio = SocketIO(app)

users = {}

@app.route("/")
def index():
    return app.send_static_file('index.html')

@socketio.on('connect')
def handle_connect():
    user_id = request.sid
    users[user_id] = {'name': 'IP ' + request.remote_addr}
    print(f"User {user_id} connected")

@socketio.on('disconnect')
def handle_disconnect():
    user_id = request.sid
    del users[user_id]
    print(f"User {user_id} disconnected")

@socketio.on('message')
def handle_message(data):
    user_id = request.sid
    emit('message', {'name': users[user_id]['name'], 'text': data['text']}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
