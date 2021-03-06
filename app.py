from flask import Flask, render_template, request, redirect,url_for
import sqlite3 as sql
import time
from flask_mail import Mail, Message
import json
import os
import smsSender

app = Flask(__name__)

try:
	with open('creds.json') as json_file:
		mailID = json.load(json_file)

except:
	print("Since this is your first time. Please provide a admin Email and password")
	email = input("Admin Email : ")
	password = input("Admin Password : ")
	mailID = {}
	mailID['id'] = email
	mailID['password'] = password

	with open('creds.json','w') as json_file:
		json.dump(mailID,json_file)

app.config['MAIL_SERVER']='smtp.gmail.com'                
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = mailID['id']                     
app.config['MAIL_PASSWORD'] = mailID['password']              
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail=Mail(app)

def sendSmsToHost(name,email,phone,checkin,hostName):
	with sql.connect("database.db") as con:
		cur=con.cursor()
		cur.execute("select * from host where name=(?)",(hostName,))
		hostDetail=cur.fetchall();
		hostPhone = (hostDetail[0][2])
		cur.close()

		smsSender.send_sms_to_host(name,email,phone,checkin,hostPhone,hostName)

def sendMailToHost(name,email,phone,checkin,hostName):
	with sql.connect("database.db") as con:
		cur=con.cursor()
		cur.execute("select * from host where name=(?)",(hostName,))
		hostDetail=cur.fetchall();
		hostEmail = (hostDetail[0][1])
		cur.close()

	print(hostEmail)

	mailMsg = Message(name+" info recieved", sender = "admin" , recipients = [hostEmail])
	mailMsg.body = "Dear "+hostName+"\nyou have following visitor: \nName : "+name+"\nEmail : "+email+"\n Phone No. : "+str(phone)+"\nCheck-In at : "+checkin
	mail.send(mailMsg)
	print("mail send to "+mailID['id'])

def sendMailToVisitor(name,phone):
	with sql.connect("database.db") as con:
		cur=con.cursor()
		cur.execute("select * from visitor where name=(?) and phone=(?)",(name,phone))
		visitorDetail=cur.fetchall()
		email = (visitorDetail[0][1])
		hostName = visitorDetail[0][3]
		checkin = visitorDetail[0][4]
		checkout = visitorDetail[0][5]
		cur.close()

		cur=con.cursor()
		cur.execute("select * from host where name=(?)",(hostName,))
		visitorDetail=cur.fetchall()
		address = visitorDetail[0][3]
		cur.close()

	mailMsg = Message(name+" : Your last visit details", sender = "admin" , recipients = [email])
	mailMsg.body = "Name : "+name+"\n Phone No. : "+str(phone)+"\nCheck-In at : "+checkin+"\nCheck-out at : "+checkout+"\nHost-Name : "+hostName+"\nAddress visited : "+address +"\nThanks for visiting!!!"
	mail.send(mailMsg)
	print("mail sent")
 
@app.route('/',methods = ['GET'])
def home():
	return render_template('home.html')

@app.route('/pin',methods= ['GET','POST'])
def pin():
	if request.method == 'GET':
		return render_template('pin.html')
	else:
		pin = request.form['pin']
		if(pin == '9876'):
			return render_template('host.html')
		else:
			msg = 'Please Enter correct Pin'
			return render_template("result.html",msg = msg)


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
			msg = "Congrats!! You are registered as a host"
		return render_template("result.html",msg = msg)

@app.route('/checkin',methods = ['POST', 'GET'])
def checkin():
	if request.method == 'GET':
		 con = sql.connect("database.db")
		 cur=con.cursor()
		 cur.execute("select name from host")
		 hostNames = cur.fetchall()
		 return render_template('checkin.html',hostNames = hostNames)
	else:
		name = request.form['name']
		email = request.form['email']
		phone = request.form['phone']
		phone = int(phone)
		host = request.form['host']
		checkin = time.ctime(int(time.time()))
		checkout = "NULL"
		with sql.connect("database.db") as con:
			cur = con.cursor()

			cur.execute("INSERT INTO visitor (name,email,phone,host,checkin,checkout) VALUES (?,?,?,?,?,?)",(name,email,phone,host,checkin,checkout))

			con.commit()
			cur.close()
			msg = "Check-In successful! You may proceed!"

		sendMailToHost(name,email,phone,checkin,host)
		sendSmsToHost(name,email,phone,checkin,host)

		return render_template("result.html",msg = msg)

@app.route('/checkout',methods = ['POST', 'GET'])
def checkout():
	if request.method == 'GET':
		return render_template('checkout.html')
	else:
		name = request.form['name']
		phone = request.form['phone']
		checkout = time.ctime(int(time.time()))

		with sql.connect("database.db") as con:
			cur=con.cursor()
			cur.execute('''UPDATE visitor set checkout = (?) where name = (?) and phone=(?)''',(checkout,name,phone))
			con.commit()
			cur.close()

		sendMailToVisitor(name,phone)
		msg = "Thanks for Visiting! Have a nice day :)"

	return render_template("result.html",msg = msg)

@app.route('/allhosts')
def allhosts():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from host")
   
   rows = cur.fetchall()
   cur.close()
   return render_template("viewH.html",rows = rows)

@app.route('/visitors')
def visitors():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from visitor")
   
   rows = cur.fetchall()

   return render_template("viewV.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True, port = 5000)