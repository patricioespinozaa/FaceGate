from flask_socketio import SocketIO
from app import app

# Instancia global de SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

def emitir_resultado(data: dict):
    """
    Emite un mensaje con el resultado de la verificación facial
    a todos los clientes conectados por WebSocket.
    """
    socketio.emit('resultado_verificacion', data)
