#!/bin/python

#Changes my router password every few minutes for the purpose of getting rid of hackers 



#The idea of this is more important than the program itself.


#This version uses the min web browser so should be more stable.
#This is a quick and ugly program,don't expect any professional programming practices here,it is designed to work for me not anyone else. I still hope that in some way it will be useful to others.

# Author - Peter Wolf
# dougalite@gmail.com
# Started 25-9-2024

#This program is specific to my router/modem and is designed for linux and may not run on another OS and almost certainly not on another type of router

#This program is the main program that should be running on a computer and the computer should not be used after running the program.Maybe us a dedicated old laptop.
#It is not advisable to run this unless you already have a very secure system.Do not run if you have valuable data connected to the internet.This will make hackers angry if they are targetting you 
# and they could disable your system causing you to lose data.  BE EXTREMELY CAREFUL!!!

# BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!!

# the router password is stored on file as text.The fact it can be easily read is not important,far more important is actually changing the router password.
# Many insecure things about this program are not important compared to changing the router password.For me, they are not worth worrying about.
# License = no license. Pretend you wrote it ,take credit for it ,modify it,sell it ,pretend it is your idea,I don't care,whatever,wouldn't be the first time to happen to me.

#designed for the following router/modem - OPTUS SAGEMCOM


#REQUIREMENTS before you run the program- 
#- min web browser
#pynput  check the web for instructions


import	random
import	re
import time
from pathlib import Path
import os
from subprocess import Popen
from pynput.keyboard import Key, Controller


keyboard=Controller()


defaultip="192.168.0.1"
minlogfile=os.getenv("HOME")+"/.config/Min/Session Storage/000003.log"
delay=30
passwfilename="routerpassword.txt"
lastipfile="lastip.txt"
passwordlength=20

def savewebpage(webpagename):
	'''Saves the current webpage with the passed name'''
	keyboard.press(Key.ctrl)
	keyboard.type("s")
	keyboard.release(Key.ctrl)
	time.sleep(2.0)
	keyboard.type(webpagename)
	time.sleep(1)
	keyboard.press(Key.enter)
	keyboard.release(Key.enter)
def	alarm():
	'''Endless loop alarm'''
	while(1):
		print("\a")
		print("Different webpage detected or fatal error of another kind.Program failure")
	
def	checkwebpage(webpagename):
	'''check modem settings webpage by searching for the word modem in it.If not there then raise alarm'''
	savewebpage(webpagename)
	time.sleep(3)
	try:
		fp=open(webpagename,"r")
		data=fp.read()
		fp.close()
	except:
		print("ERROR! Cannot read saved webpage!")
		alarm()
	m=re.search("Modem",data)
	if m.span==[0,0]:
		alarm()


def quitbrowserkeys():
    """does keypresses to quit min browser """
    keyboard.press(Key.ctrl)
    keyboard.type("q")
    keyboard.release(Key.ctrl)

def	presstab(repeats):
	"""simulates a tab keypress with small delays """
	for i in range(repeats):
		time.sleep(0.3)
		keyboard.type('\t')
		time.sleep(0.3)

def	pseudorandompassword (plength):
		""" returns a very simple psuedo random password of roughly specified length """
		choice=["HBR1.com","934W:a","grb<0>"]
		ret=choice[random.randint(0,len(choice)-1)]
		for i in range(plength):
			ret+=chr(ord("a")+random.randint(1,26))
		return(ret)
def logout():
	"""logout of router"""
	presstab(3)
	keyboard.press(Key.enter)
	keyboard.release(Key.enter)
	time.sleep(10)


print("This program is specific to my router/modem and may not be useful for anyone else.It is not advisable to run this unless you already have a very secure system.Do not run if you have valuable data connected to the internet.This will make hackers angry if they are targetting you  and they could disable your system causing you to lose data.  BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!! BE EXTREMELY CAREFUL!!!")


lp=Path(lastipfile)
try:
	candidateip=lp.open().readline().strip()
except:	
	candidateip=defaultip


print("Last router ip = ",candidateip)
routerip=input("Enter new router ip address,press enter for last used router ip.  ")
if len(routerip)<4 or len(routerip)>15:
	routerip=candidateip
else:
	lp.open("w").write(routerip)
	
password=input("Enter router password or press enter to use a saved one.  ")

p=Path(passwfilename)
if len(password)<4 or len(password)>50:
	try:
		password=p.open().readline().strip()

	except:
		password="whatever345"
#Get min in cache
devnull = open(os.devnull, 'wb')
if	not os.path.isfile(minlogfile):
	print("Getting min into the cache,please wait about a minute.")
	Popen(['min'], stdout=devnull, stderr=devnull)
	time.sleep(40)
print("Starting min .If not logged into router there will be an iniital false login error,just wait for a real login attempt.\n")
Popen(['min', "http://"+routerip], stdout=devnull, stderr=devnull)

time.sleep(20)
savewebpage("/tmp/test.html")
time.sleep(7)
logout()#logout of router if accidentally logged in	
	
loop=0
while 1:

	newpassword=pseudorandompassword(passwordlength)
	print( "Candidate new password is ",newpassword)

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
	checkwebpage("/tmp/temp.html")

	presstab(17)
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
	password=newpassword
	print("Password changed ",loop," times")
	time.sleep(delay)


