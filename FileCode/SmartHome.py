#!/usr/bin/env python
import logging
import time
import json
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from rpi_lcd import LCD
import threading
import Adafruit_DHT
from threading import Lock
from time import sleep
import time
import serial
import sys
import pyrebase


#________________________________API_FIREBASE___________________________________
config = {
  "apiKey": "AIzaSyBHNGXFfqAM0zBQOgTUM9YvByNmbnD474E",
  "authDomain": "rasp-firebase-d317a.firebaseapp.com",
  "databaseURL": "https://rasp-firebase-d317a-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "rasp-firebase-d317a",
  "storageBucket": "rasp-firebase-d317a.appspot.com",
  "messagingSenderId": "235103114637",
  "appId": "1:235103114637:web:5cacb5bdd533336b08d9c4",
  "measurementId": "G-LJCB645TTH"
};
#__________________________________GPIO.OUTPUT__________________________________
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#garage
GPIO.setup(12,GPIO.OUT)
#Main door
GPIO.setup(13,GPIO.OUT)
#servo = Servo(13)
#Khoang cach out(trigger)
GPIO.setup(24,GPIO.OUT)
#LED
GPIO.setup(20,GPIO.OUT)
#BUZZER
GPIO.setup(5,GPIO.OUT)

#___________________________________GPIO.INPUT_________________________________
#Sound
GPIO.setup(16,GPIO.IN)
#rain sensor
GPIO.setup(17,GPIO.IN)
#touch
GPIO.setup(25,GPIO.IN)
#khoang cach in(echo)
GPIO.setup(23,GPIO.IN)
#PIR
GPIO.setup(4,GPIO.IN)
DHT = Adafruit_DHT.DHT11

#__________________________________FIREBASE__________________________________
def thread_firebase_iot(flag,key,parameter_gas,parameter_temp,db):
	print("Firebase_Iot: ON")
	firebase = pyrebase.initialize_app(config)
	while True:
		time.sleep(0.1)
		database = firebase.database()
		db[0] = database.child("Gate").get()
		db[1] = database.child("Led").get()
		db[2] = database.child("Windown").get()
		db[3] = database.child("Fire").get()
		db[4] = database.child("Garage").get()
		db[5] = database.child("Door").get()
		

		
#____________________________________________________________________
def thread_firstget(flag,key,db):
	print("firstget : ON")
	time.sleep(4)
	while True:
		time.sleep(0.5)
		#Fire
		if db[3].val() == "on" and key[3] == 0 and key[2] ==  0 :
			key[2] = 1
			mogate()
		elif db[3].val() == "on" and key[3] == 1 and key[2] ==  0 :
			key[2] = 1
			mogate()
			dongcuaso()
			flag[3] = flag[3] + 1
			key[3] = 0
		elif db[3].val() == "off" and key[2] == 1:
			key[2] = 0
			donggate()
		
		#Gate
		if db[0].val() == "on" and key[0] == 0 and key[2] == 0:
			key [0] = 1
			mogate()
		elif db[0].val() == "off" and key[0] == 1 and key[2] == 0:
			donggate()
			key [0] = 0

		#LedRoom
		if db[1].val() == "on" and key[1] == 0 and key[2] == 0:
			flag[1] = flag[1] + 1
		elif db[1].val() == "off" and key[1] == 1 and key[2] == 0:
			flag[1] = flag[1] + 1
		
		
def thread_secondget(flag,key,db):
	print("secondget: ON")
	time.sleep(4)
	while True:
		time.sleep(0.5)
		#Windown
		if db[2].val() == "on" and key[3] == 0 and flag[3] % 2 == 0:
			print("hceck")
			flag[3] = flag[3] + 1
			time.sleep(0.5)
		elif db[2].val() == "off" and key[3] == 1 and flag[3] % 2 != 0:
			print("dong")
			flag[3] = flag[3] + 1
			time.sleep(0.5)

		#Garage
		if db[4].val() == "on" and key[5] == 0:
			key[5] = 1
			mogarage()			
		elif db[4].val() == "off" and key[5] == 1:
			donggarage()
			key[5] = 0

		#Maindoor
		if db[5].val() == "on" and key[6] == 0:
			flag[5] = flag[5] + 1
			print(flag[5])		
		elif db[5].val() == "off" and key[6] == 1:
			flag[5] = flag[5] + 1
#_______________________________GARAGE_________________________________
pwm_garage = GPIO.PWM(12,60)
pwm_garage.start(13.5)
def mogarage():
	GPIO.output(5,1)
	time.sleep(0.3)
	GPIO.output(5,0)
	pwm_garage.ChangeDutyCycle(7.5)
	
def donggarage():
	GPIO.output(5,1)
	time.sleep(0.3)
	GPIO.output(5,0)
	pwm_garage.ChangeDutyCycle(13.5)


#________________________________MAINDOOR______________________________
pwm_door = GPIO.PWM(13,60)
pwm_door.start(7.5)

def mocua(key):
	
	pwm_door.ChangeDutyCycle(12.5)
	if key[7] == 0:
		GPIO.output(5,1)
		time.sleep(0.3)
		GPIO.output(5,0)
	
def dongcua(key):
	if key[7] == 0:
		GPIO.output(5,1)
		time.sleep(0.3)
		GPIO.output(5,0)
	pwm_door.ChangeDutyCycle(7.5)
	

def distance():
	GPIO.output(24, True)
	
	time.sleep(0.00001)
	GPIO.output(24, False)
 	
	StartTime = time.time()
	StopTime = time.time()
	
	while GPIO.input(23) == 0:
		StartTime = time.time()
		 	
	while GPIO.input(23) == 1:
		StopTime = time.time()
		print("check")
	TimeElapsed = StopTime - StartTime
	distance = (TimeElapsed * 34300) / 2
 
	return distance

def thread_maindoor(flag,key):
	print("MainDoor: ON")
	while True:
		time.sleep(0.5)
		if GPIO.input(25) == 1:
			key[6] = 1
			key[7] = 0
			mocua(key)
			time.sleep(4)
			dongcua(key)
			key[6] = 0 

		if flag[5] % 2 != 0 and key[6] == 0:
			key[6] = 1
			key[7] = 1
			mocua(key)
			
		elif flag[5] != 0 and flag[5] % 2 == 0 and key[6] == 1:
			key[7] = 1
			dongcua(key)
			
			key[6] = 0 
			

#________________________________LEDROOM________________________________
def thread_led(flag,key):
	while True:
		time.sleep(1)
		if flag[1] % 2 != 0:
			GPIO.output(20,1)
			key[1] = 1
		elif flag[1] % 2 == 0:
			GPIO.output(20,0)
			key[1] = 0

def thread_led_mic(flag,key):
	print("LedRoom: ON")
	while True:
		if GPIO.input(16) == 1:
			flag[1] = flag[1] + 1
			time.sleep(0.5)

#_________________________________UART_________________________________
ser = serial.Serial(
	port = '/dev/ttyAMA0',
	baudrate = 9600,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)
#_________________________________LCD___________________________________
def LCD1(parameter_gas,parameter_temp):
	lcd = LCD()
	print("LCD : ON")
	firebase = pyrebase.initialize_app(config)
	while True:
		
		do_am, nhiet_do = Adafruit_DHT.read_retry(DHT, 21);
		
		s = ser.readline()
		data = s.decode()			
		data = data.rstrip()			
		
		parameter_gas = int(data)
		parameter_temp = nhiet_do
		
		lcd.text("Gas: {}".format(parameter_gas),1)
		lcd.text("Temp: {}%C".format(parameter_temp),2)
		database = firebase.database()
		data1 = {"gas": str(parameter_gas),
			"temperature": str(int(parameter_temp))			}
		database.update(data1)

		time.sleep(0.4)

#_________________________________GATE___________________________________

def mogate():
	print("cung")
	ser.write(b'mocong')
	ser.flush()
def donggate():
	ser.write(b'dongcong')
	ser.flush()

#_________________________________WINDONW___________________________________
def mocuaso():
	ser.write(b'mocuaso')
	ser.flush()
	
def dongcuaso():
	ser.write(b'dongcuaso')
	ser.flush()
	
def thread_CuaSo(flag,key):
	print("Cua So :ON")
	while True:
		time.sleep(1)
		if flag[3] % 2 != 0 and key[3] == 0 and key[2] == 0:
			key[3] = 1
			print("mo cua so")
			mocuaso()
		elif flag[3] % 2 == 0 and key[3] == 1 and key[2] ==0:
			print("dong cua so")
			dongcuaso()
			key[3] = 0
		
#__________________________________MAIN_FUNCTION_____________________________
if __name__ == '__main__':
	parameter_gas = 0 #Gas
	parameter_temp = 0 #Gas
	db = ["e","e","e","e","e","e"] # Gate,LedRoom,CuaSo,Fire,Garage,MainDoor
	flag = [0,0,0,0,0,0] # Gate,LedRoom,temp,CuaSo,Fire,MainDoor
	key = [0,0,0,0,0,0,0,0] # Gate,LedRoom,temp,CuaSo,Fire,Garage,MainDoor,coi

#__________________________________THREADING_______________________________

	firebase = threading.Thread(target = thread_firebase_iot,args = (flag,key,parameter_gas,parameter_temp,db))
	led = threading.Thread(target = thread_led,args = (flag,key))
	lcd = threading.Thread(target = LCD1,args = (parameter_gas,parameter_temp))
	thread_firstget = threading.Thread(target = thread_firstget,args = (flag,key,db))
	thread_secondget = threading.Thread(target = thread_secondget,args = (flag,key,db))
	led_mic = threading.Thread(target = thread_led_mic,args = (flag,key))
	cuaso = threading.Thread(target = thread_CuaSo,args = (flag,key))
	thread_maindoor = threading.Thread(target = thread_maindoor,args = (flag,key))

#____________________________________THREAD.START______________________
	thread_maindoor.start()
	thread_firstget.start()
	thread_secondget.start()
	lcd.start()
	led.start()
	led_mic.start()
	cuaso.start()
	firebase.start()

    


