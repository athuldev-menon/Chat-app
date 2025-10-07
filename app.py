import os
from datetime import datetime
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb+srv://sreyas:LGAxY9cwZynotQuT@cluster0.mhetipw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

app = Flask(__name__, static_folder='static', template_folder='templates')
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='threading')

# MongoDB setup
client = MongoClient(MONGODB_URI)
db = client["chatdb"]

messages_coll = db.messages

ROOM = 'public'

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')
    recent = list(messages_coll.find().sort('ts', 1))
    for m in recent:
        emit('message', {
            'user': m.get('user', 'anonymous'),
            'text': m.get('text', ''),
            'ts': m.get('ts').isoformat() if isinstance(m.get('ts'), datetime) else m.get('ts')
        })
    join_room(ROOM)

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')

@socketio.on('send_message')
def handle_send_message(data):
    user = data.get('user', 'anonymous')
    text = data.get('text', '')
    if not text:
        return
    msg = {
        'user': user,
        'text': text,
        'ts': datetime.now()
    }
    messages_coll.insert_one(msg)
    emit('message', {
        'user': user,
        'text': text,
        'ts': msg['ts'].isoformat()
    }, room=ROOM)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)
