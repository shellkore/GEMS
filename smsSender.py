import requests

try:
	with open('fast2sms_api_key.txt','r') as file:
		api_key = file.read()
except:
	print("Sms Service not configured. Please enter you fast2SMS API Key below:")
	api_key = input("Enter you key here : ")

	with open('fast2sms_api_key.txt','w') as file:
		file.write(api_key)

url = "https://www.fast2sms.com/dev/bulk"

def send_sms_to_host(name,email,phone,checkin,hostPhone,hostName):
	msg = "Dear "+hostName+"you have following visitor: \nName : "+name+"\nEmail : "+email+"\n Phone No. : "+str(phone)+"\nCheck-In at : "+checkin
	payload = "sender_id=FSTSMS&message="+msg+"&language=english&route=p&numbers="+str(hostPhone)

	headers = {
	'authorization': api_key,
	'Content-Type': "application/x-www-form-urlencoded",
	'Cache-Control': "no-cache",
	}
	response = requests.request("POST", url, data=payload, headers=headers)
