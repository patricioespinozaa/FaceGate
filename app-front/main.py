# -*- coding: utf-8 -*-
import os
import json
from app import app
from flask import request, redirect, url_for, render_template, jsonify


@app.route('/facegate/app-front/')
def index_form():
    return render_template('index.html')

@app.route('/facegate/app-front/student')
def student_form():
    return render_template('student.html')

if __name__ == "__main__":
    app.run(port=8910)
