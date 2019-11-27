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
		phone = int(phone)
		address = request.form['address']
		with sql.connect("database.db") as con:
			cur = con.cursor()

			cur.execute("INSERT INTO host (name,email,phone,address) VALUES (?,?,?,?)",(name,email,phone,address))

			con.commit()
			cur.close()
			msg = "Record successfully added"
		return render_template("result.html",msg = msg)

@app.route('/viewH')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from host")
   
   rows = cur.fetchall()
   for row in rows:
   	print(row['name'])
   	
   return render_template("viewH.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True, port = 5000)