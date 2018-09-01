import paho.mqtt.client as mqttClient
import time
import csv
# note print commands left in, to aid debugging, but commented out

broker_address = '192.168.1.20'  # enter your broker details here
port = 1885
user = 'your username here'
password = 'your password here'

def on_connect(client, userdata, flags, rc):   
     if rc == 0:
         print("Connected to broker") 
         global Connected                #Use global variable
         Connected = True                #Signal connection 
     else: 
        print("Connection failed")
 
def on_message(client, userdata, message):     # define call backs
	data = message.payload
	data = data.decode("ascii")
	#print (data)								# left the print in - so you can de-bug
	mList = [int(e) if e.isdigit() else e for e in data.split(',')]
	#print (mList)
	#print(*mList, sep='\n')
	#for row in mList:
		# if row != "":
	#	print(mList[row])
	#print (mList[2])
	
	if mList[2] == 'WGR800':   								# wind sensor
	#OS,WGR800,187,0,OK,,,,,0.000,0.400,247.500,,,,
		gust = mList[10]
		average = mList[11]
		direction = mList[12]
		#print ('gust ' + gust)
		#print ('average ' + average)
		#print ('direction  ' + direction)
		client.publish("Oregon/gust", gust)
		client.publish("Oregon/average", average)
		client.publish("Oregon/direction", direction)
		
	if mList[2] == 'THGR810':  								# temp & humidity sensor
	#OS,THGR810,187,1,OK,22.800,40,,,,,,,,,
	#or
	#2018-07-07 17:48:41,OS,THGR810,187,1,OK,33.300,39,,,,,,,,,
		temperature = mList[6]
		humidity = mList[7]
		a = str(temperature)
		b = str(humidity)
		#print ('temperature  ' + a)
		#print ('humidity  ' + b)
		client.publish("Oregon/temp", a)
		client.publish("Oregon/humidity", b)
		
	if mList[2] == 'PCR800':   								#rain sensor
	#OS,PCR800,253,0,OK,,,0.000,1.147,,,,,,,
	#or
	#2018-07-07 17:49:19,OS,PCR800,253,0,OK,,,0.000,1.147,,,,,,,
		rain_rate = mList[8]
		rain_total = mList[9]
		#print ('rain_rate  ' + rain_rate)
		#print ('rain_total  ' + rain_total)
		client.publish("Oregon/rain_rate", rain_rate)
		client.publish("Oregon/rain_total", rain_total)
	
	if mList[2] == "Acurite tower sensor":  					#its an (Acurite) sensor
		#,Acurite tower sensor,11794,A,,22.700,41,,,,,,,,,
		#or
		#2018-07-07 17:49:26,,Acurite tower sensor,11794,A,,28.200,44,,,,,,,,,
		#print("Acurite tower")
		if mList[6] != "":
			temperature = mList[6]
			a = str(temperature)
			#print ('temperature Acurite  ' + a)
			client.publish("acurite/temp", a)
			mList[6] = ""									# trying to avoid duplicate messages (and failing)
		if mList[7] != "":
			humidity = mList[7]
			b = str(humidity)
			#print ('humidity Acurite  ' + b)
			client.publish("acurite/humidity", b)
			mList[7] = ""
		
	
Connected = False   #global variable for the state of the connection

client = mqttClient.Client("Python")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
 
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
client.subscribe("home/rtl_433")
 
try:
    while True:
        time.sleep(1)
 
except KeyboardInterrupt:
   # print ("exiting")
    client.disconnect()
    client.loop_stop()