from flask_socketio import SocketIO, emit

# Instancia global de SocketIO
socketio = SocketIO(cors_allowed_origins="*")

def emitir_resultado(data: dict):
    """
    Emite un mensaje con el resultado de la verificación facial
    a todos los clientes conectados por WebSocket.
    """
    socketio.emit('resultado_verificacion', data)

@socketio.on('offer')
def handle_offer(data):
    emit('offer', data, broadcast=True, include_self=False)

@socketio.on('answer')
def handle_answer(data):
    emit('answer', data, broadcast=True, include_self=False)

@socketio.on('ice-candidate')
def handle_ice_candidate(data):
    emit('ice-candidate', data, broadcast=True, include_self=False)