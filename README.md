# GEMS - General-Entry-Management-Software

## TABLE OF CONTENT
+ [DESCRIPTION](https://github.com/shellkore/entry-management-software#description)
+ [FEATURES](https://github.com/shellkore/entry-management-software#description)
+ [REQUIREMENTS](https://github.com/shellkore/entry-management-software#requirements)
+ [HOW TO RUN](https://github.com/shellkore/entry-management-software#how-to-run)
+ [WORKFLOW](https://github.com/shellkore/entry-management-software#workflow)
+ [APPROACH](https://github.com/shellkore/entry-management-software#approach)
+ [REPO-DESCRIPTION](https://github.com/shellkore/entry-management-software#repo-description)
	

## DESCRIPTION
This is an entry management software built on flask. This is made for the purpose of innovacer summergeeks-SDE.

Live Link deployed on heroku [here](https://ems-shellkore.herokuapp.com)

## FEATURES
+ Host can register itself with name, mail, phone no. and address.
+ Visitor have two options - check-in and check-out
+ In check-in option the user details to be provided are: name, email, phone and host which he/she is visiting.
+ Visitor's details are added in Database along with it's entry timestamp as checkin time.
+ As soon as visitor check-in, a **mail and a SMS to the corresponding host** is sent of the arrival.
+ On leaving the place, visitor do check-out. Details to be provided are name and phone no. only.
+ As soon as visitor do check-out, a **mail to the visitor** is sent of all his details along with the address of host he/she visited.
+ You can view Database (hosts and visitors) by '/viewH' and 'viewV' links.

## REQUIREMENTS
install all requirements from requirement.txt

`pip3 install -r requirements.txt`

## HOW TO RUN

Make sure you have all the requirements installed mentioned above.

+ run createDB.py to create database.
  `python3 createDB.py`
+ run app.py
  `python3 app.py`
+ open browser and enter `127.0.0.1:5000`
+ Rest is self-explanatory
+ To view all your hosts
	`127.0.0.1:5000/viewH`
+ To view all your visitors
	`127.0.0.1:5000/viewV`

## WORK-FLOW

+ Database can be viwed with the help of
	+ Host `127.0.0.1:5000/viewH`
	![host-db](images/host_shellkore.png)
	+ Visitor '127.0.0.1:5000/viewV'
	![visitor-db](images/before_tester.png)

+ To add a host
![host](images/host.png)

+ To check in by visitor
![checkin](images/checkin.png)

+ Database after visiter do check-in
![after-checkin](images/after_tester.png)

+ Mail sent to Host
![mail-host](images/host_mail.png)

+ SMS sent to Host

![sms-host](https://user-images.githubusercontent.com/36515927/69811713-af6ca400-1214-11ea-9c4e-c12f59916d8b.png)

+ To check-out by visitor
![check-out](images/checkout.png)

+ Database after checkout
![after-checkout](images/after_tester_checkout.png)

+ Mail sent to the visitor about his visit
![visitor_mail](images/visitor_mail.png)

## APPROACH

1. **Front-End** made using HTML/CSS. These files are kept in templates folder for flask to read them. The forms made consist of corresponding field:
	+ name : type="text"
	+ E-Mail : type="email"
	+ Phone Number : type="number" etc.
	
1. Database is designed in sqlite3. There are two tables.
	+ Host : 
		+ name TEXT,
		+ email TEXT, 
		+ phone INTEGER NOT NULL PRIMARY KEY,
		+ address TEXT
	+ Visitor :
		+ name TEXT, 
		+ email TEXT, 
		+ phone INTEGER NOT NULL PRIMARY KEY, 
		+ host TEXT,
		+ checkin TEXT, 
		+ checkout TEXT

1. **Flask**: this front-end is connected with database with the help of Flask app created in python. The routes created in Flask are:
	+ @app.route('/',methods = ['POST', 'GET']) : for landing on home-page which is checkin in our case.
	+ @app.route('/host',methods = ['POST', 'GET']) : for host registration.
	+ @app.route('/checkout',methods = ['POST', 'GET']) : gor check-out.
	+ @app.route('/viewH') : to view all hosts
	+ @app.route('/viewV') : to view all visitors
	Also there are 3 functions:
		+ sendSmsToHost(name,email,phone,checkin,hostName) : to send sms to host when visitor checks in.
		+ sendMailToHost(name,email,phone,checkin,hostName) : to send mail to host when user checks in.
		+ sendMailToVisitor(name,phone) : to mail visitor their detail when they do check-out.

## REPO-DESCRIPTION
+ images : contains images for work-flow.
+ static/styles : contain CSS file for styling.
+ templates : contains all HTML files.
+ .gitignore : contains name of file which contains info which can't be exposed to public. eg: API authentication keys and password.
+ Procfile : contains server info. required for deploying on Heroku.
+ README.md : Contains documentation.
+ app.py : main file of the project. Contains flask app code in it.
+ createDB.py : this file is required to create DB in sqlite3 at the beginning.
+ database.db : contains Sqlite3 data. All information entered is saved in this file.
+ requirements.txt : requirements means all the libraries required for running our program.
+ smsSender.py : python file to send sms to host.

>This is made for the purpose of internship selection task only. Please don't create issues and send PRs. Thanks.
