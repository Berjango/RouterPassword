#!/bin/python

#Changes my router password every few minutes for the purpose of getting rid of hackers 

#The idea of this is more important than the program itself.

#This is a quick and ugly program,don't expect any professional programming practices here,it is designed to work for me not anyone else. I still hope that in some way it will be useful to others.

# Author - Peter Wolf
# dougalite@gmail.com
# Started 25-9-2024

#This program is specific to my router/modem and is designed for linux and may not run on another OS and almost certainly not on another type of router

#Designed for a live system running from DVD or USB,not so useful for a HDD or SSD based system

#It is not advisable to run this unless you already have a very secure system.Do not run if you have valuable data connected to the internet.This will make hackers angry if they are targetting you 
# and they could disable your system causing you to lose data.  BE EXTREMELY CAREFUL!!!

# BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!!

# the router password is stored on file as text.The fact it can be easily read is not important,far more important is actually changing the router password.
# Many insecure things about this program are not important compared to changing the router password.For me, they are not worth worrying about.
# License = no license. Pretend you wrote it ,take credit for it ,modify it,sell it ,pretend it is your idea,I don't care,whatever,wouldn't be the first time to happen to me.

#designed for the following router/modem - OPTUS SAGEMCOM


#REQUIREMENTS before you run the program- 
#- Firefox web browser
#pynput  check the web for instructions

import	random
import time
from pathlib import Path
import os
from subprocess import Popen


from pynput.keyboard import Key, Controller


keyboard=Controller()
defaultip="192.168.0.1"

delay=30

passwfilename="routerpassword.txt"
lastipfile="lastip.txt"

passwordlength=20


def	presstab(repeats):
	"""simulates a tab keypress with small delays """
	for i in range(repeats):
		time.sleep(0.1)
		keyboard.type('\t')
		time.sleep(0.1)

def	pseudorandompassword (plength):
		""" returns a very simple psuedo random password of roughly specified length """
		ret="HBR1.com"
		for i in range(plength):
			ret+=chr(ord("a")+random.randint(1,26))
		return(ret)


print("This program is specific to my router/modem and may not be useful for anyone else.It is not advisable to run this unless you already have a very secure system.Do not run if you have valuable data connected to the internet.This will make hackers angry if they are targetting you  and they could disable your system causing you to lose data.  BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!!")


lp=Path(lastipfile)
try:
	candidateip=lp.open().readline()
except:	
	candidateip=defaultip


print("Last router ip = ",candidateip)
routerip=input("Enter new router ip address,press enter for last used router ip.  ")
if len(routerip)<4 or len(routerip)>15:
	routerip=candidateip
else:
	lp.open("w").write(routerip)
	
password=input("Enter password or press enter to use a saved one.  ")

lp=Path(lastipfile)
p=Path(passwfilename)
if len(password)<4 or len(password)>50:
	try:
		with p.open() as f:
			password=f.readline()
			p.close()
	except:
		password="whatever345"

devnull = open(os.devnull, 'wb')
Popen(['firefox', "http://"+routerip,"-safe-mode"], stdout=devnull, stderr=devnull)

time.sleep(30)
	
loop=0
while 1:

	newpassword=pseudorandompassword(passwordlength)
	print( "New password is ",newpassword)
	
	keyboard.type('optus')			#log in to router here
	presstab(1)
	keyboard.type(password)
	presstab(1)
	keyboard.press(Key.enter)
	keyboard.release(Key.enter)
	time.sleep(10)
	print("Logged in to router.")
  
	presstab(5)				#Navigate to modem settings
	keyboard.press(Key.enter)
	keyboard.release(Key.enter)
	
	time.sleep(10)
	print("In modem settings.")

	presstab(26)
	keyboard.press(Key.enter)		#Navigate to password section
	keyboard.release(Key.enter)
	print("In password section.")
	time.sleep(10)

	presstab(1)			#Input new passwords
	keyboard.type(password)
	presstab(1)
	keyboard.type(newpassword)
	presstab(1)
	keyboard.type(newpassword)
	presstab(3)
	keyboard.press(Key.enter)
	keyboard.release(Key.enter)
	
	print("Changed password to ",newpassword)

	p.open("w").write(newpassword)
	loop+=1
	print("Password changed ",loop," times")
	time.sleep(delay)


