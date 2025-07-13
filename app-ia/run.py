import eventlet
eventlet.monkey_patch()

from app import app
from config.settings import PORT
from services.socket_events import socketio
import main

socketio.init_app(app)

if __name__ == '__main__':
    socketio.run(app, port=PORT, debug=False)