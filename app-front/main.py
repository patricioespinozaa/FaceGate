# -*- coding: utf-8 -*-
import os
import json
from app import app, socketio
from flask import request, redirect, url_for, render_template, jsonify


@app.route('/facegate/app-front/')
def index_form():
    return render_template('index.html')

@app.route('/facegate/app-front/student')
def student_form():
    return render_template('student.html')

# =======================
# WebSocket Handlers
# =======================

@socketio.on('connect')
def handle_connect():
    print('🔌 Cliente conectado')

@socketio.on('disconnect')
def handle_disconnect():
    print('❌ Cliente desconectado')

@socketio.on('offer')
def handle_offer(data):
    print('📡 Oferta WebRTC recibida')
    socketio.emit('offer', data)

@socketio.on('answer')
def handle_answer(data):
    print('📡 Respuesta WebRTC recibida')
    socketio.emit('answer', data)

@socketio.on('ice-candidate')
def handle_candidate(data):
    print('❄️ Candidato ICE recibido')
    socketio.emit('ice-candidate', data)


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8910)
