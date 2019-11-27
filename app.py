from flask import Flask, render_template, request, redirect,url_for
from flask_mail import Mail, Message
import sqlite3 as sql
import time

app = Flask(__name__)

@app.route('/')
def home():
   return ('Success') 

@app.route('/host',methods = ['POST', 'GET'])
def host():
	if request.method == 'GET':
		return render_template('host.html')
	else:
		name = request.form['name']
		email = request.form['email']
		phone = request.form['phone']
		address = request.form['address']
		print(type(name))
		print(name)
		print(email)
		print(type(phone))
		print(type(address))
		msg = "read succesfully"
		return render_template("result.html",msg = msg)


if __name__ == '__main__':
   app.run(debug = True, port = 5000)