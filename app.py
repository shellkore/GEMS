from flask import Flask, render_template, request, redirect,url_for
from flask_mail import Mail, Message
import sqlite3 as sql
import time

app = Flask(__name__)

@app.route('/')
def home():
   return ('Success') 

if __name__ == '__main__':
   app.run(debug = True, port = 5000)