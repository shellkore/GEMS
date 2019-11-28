from flask import Flask, render_template, request, redirect,url_for
import sqlite3 as sql
import time
from flask_mail import Mail, Message
import json

app = Flask(__name__)


with open('creds.json') as json_file:
		mailID = json.load(json_file)

print(mailID['id'])
print(mailID['password'])

app.config['MAIL_SERVER']='smtp.gmail.com'                
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = mailID['id']                     
app.config['MAIL_PASSWORD'] = mailID['password']              
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail=Mail(app)

def sendMailToHost(name,email,phone,checkin,hostName):
	with sql.connect("database.db") as con:
		cur=con.cursor()
		cur.execute("select * from host where name=(?)",(hostName,))
		hostDetail=cur.fetchall();
		hostEmail = (hostDetail[0][1])
		cur.close()

	print(hostEmail)

	mailMsg = Message(name+" info recieved", sender = "admin" , recipients = [hostEmail])
	mailMsg.body = "Name : "+name+"\nEmail : "+email+"\n Phone No. : "+str(phone)+"\nCheck-In at : "+checkin
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
			msg = "Record successfully added in host"
		return render_template("result.html",msg = msg)

@app.route('/chekin',methods = ['POST', 'GET'])
def checkin():
	if request.method == 'GET':
		return render_template('checkin.html')
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
			msg = "Record successfully added in visitor"

		sendMailToHost(name,email,phone,checkin,host)

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
		msg = "Visitor checkout successful"

	return render_template("result.html",msg = msg)

@app.route('/viewH')
def viewH():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from host")
   
   rows = cur.fetchall()

   return render_template("viewH.html",rows = rows)

@app.route('/viewV')
def viewV():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from visitor")
   
   rows = cur.fetchall()

   return render_template("viewV.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True, port = 5000)