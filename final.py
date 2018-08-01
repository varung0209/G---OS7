import os
import psutil
import webbrowser
import math
import subprocess
import platform

from fuzzywuzzy import fuzz
from flask import Flask
from flask_ask import Ask, statement, question, delegate,session
from twilio.rest import Client

TWILIO_PHONE_NUMBER = "+18053358898"
WIML_INSTRUCTIONS_URL = "http://static.fullstackpython.com/phone-calls-python.xml"
client = Client("AC7b97a7a6264813fafd695f02b7b071a5", "4502047c06369e5aa4f1a436d0787c88")
calllist = {"varun":"+918147486031","purva":"+919900376300","gaurav":"+919591337273",}
names = calllist.keys
pagelist = {"Google":"https://www.google.com/","Facebook":"https://www.facebook.com/","Twitter":"https://twitter.com/","Netflix":"https://www.netflix.com/in/","Prime Video":"https://www.primevideo.com/","Youtube":"https://www.youtube.com/","Quora":"https://www.quora.com/",}
pages = pagelist.keys

app = Flask(__name__)
ask = Ask(app, "/")

def get_dialog_state():
	return session['dialogState']

def sectohour(secs):
	mm, ss = divmod(secs, 60)
	hh, mm = divmod(mm, 60)
	hh1 = int(math.fabs(hh))
	return (hh1, mm, ss)

def get_path():
	f = psutil.disk_partitions()
	n = len(f)
	path = list()
	for i in range(0, n):
		if f[i][2] != '':
			path.append(f[i][1])
	return path


@ask.launch
def launch():
	speech_text = 'Ghost Protocol Initiated.'
	return question(speech_text)


@ask.intent('retrieve_percentage')
def ret_battery():
	battery = psutil.sensors_battery()
	(hh, mm, ss) = sectohour(battery.secsleft)
	if(battery.power_plugged == True):
		speech_text = 'Battery Percentage is %s Percent. \n Time left is %s hour %s minutes. \n Status : Charging.'%(battery.percent,hh, mm)
	else:
		speech_text = 'Battery Percentage is %s Percent.\n Time left is %s hour %s minutes. \n Status : Discharging.'%(battery.percent,hh, mm)
	return question(speech_text)


@ask.intent('access_file')
def accessfile(file_name):
	dialog_state = get_dialog_state()
	if dialog_state != 'COMPLETED':
		return delegate()
	name = file_name.split('.')
	speech_text = None
	if os.name == 'posix':
		dir_path = os.path.dirname(os.environ['HOME'])
		for root, dirs, files in os.walk(dir_path):
			for file in files:
				if file.endswith('.'+name[1]):
					d = fuzz.token_set_ratio(file, name[0])
					if d>=80:
						matches=(root + '/'+str(file))
						os.system('gedit %s'%matches)
						speech_text = 'File %s opened in Editor from path %s'%(name[0],matches)
		if speech_text==None:
			os.system('gedit %s'%file_name)
			speech_text = 'File %s created in path %s'%(name[0],homedir)
		speech_text = 'File open in Editor %s'%file_name
	elif os.name == 'nt':
		path = get_path()
		for drive in path:
			for root, dirs, files in os.walk(drive):
				for file in files:
					d = fuzz.token_set_ratio(file, file_name)
					if d>=80:
						matches=(root + '/'+str(file))
						subprocess.call(['notepad.exe', matches])
						speech_text = 'File %s from path %s'%(name[0],matches)
		if speech_text==None:
			subprocess.call(['notepad.exe', 'file_name'])
			speech_text = 'file created %s in desktop'%file_name
	return question(speech_text)


@ask.intent('play_file')
def play_music(file_type,file_name):
	dialog_state = get_dialog_state()
	if dialog_state != 'COMPLETED':
		return delegate()
	if os.name == 'posix':
		dir_path = os.path.dirname(os.environ['HOME'])
		if file_type == 'song' or file_type == 'music':
			for root, dirs, files in os.walk(dir_path):
				for file in files:
					if file.endswith('.mp3'):
						d = fuzz.token_set_ratio(file, file_name)
						if d>=80:
							matches=(root + '/'+str(file))
							speech_text = 'Playing %s on System'%file_name
							webbrowser.open(matches)
							return question(speech_text)
						else:
							speech_text = 'Unable to find file %s'%file_name
		if file_type == 'video' or file_type == 'movie':
			for root, dirs, files in os.walk(dir_path):
				for file in files:
					if file.endswith('.mp4'):
						d = fuzz.token_set_ratio(file, file_name)
						if d>=80:
							matches=(root + '/'+str(file))
							speech_text = 'Playing %s on System'%file_name
							webbrowser.open(matches)
							return question(speech_text)
						else:
							speech_text = 'Unable to find file %s'%file_name
	elif os.name == 'nt':
		path = get_path()
		if file_type == 'song' or file_type == 'music':
			for drive in path:
				for root, dirs, files in os.walk(drive):
					for file in files:
						if file.endswith('.mp3'):
							d = fuzz.token_set_ratio(file, file_name)
							if d>=80:
								matches=(root + '/'+str(file))
								speech_text = 'Playing on System'
								webbrowser.open(matches)
								return question(speech_text)
							else:
								speech_text = 'Unable to find file'
				return question(speech_text)
		if file_type == 'video' or file_type == 'movie':
			for drive in path:
				for root, dirs, files in os.walk(drive):
					for file in files:
						if file.endswith('.mp4'):
							d = fuzz.token_set_ratio(file, file_name)
							if d>=80:
								matches=(root + '/'+str(file))
								speech_text = 'Playing on System'
								webbrowser.open(matches)
								return question(speech_text)
							else:
								speech_text = 'Unable to find file'
	return question(speech_text)


@ask.intent('run_file')
def execute_file(file_name):
	dialog_state = get_dialog_state()
	if dialog_state != 'COMPLETED':
		return delegate()
	speech_text = None
	if os.name == "posix":
		path = '/usr/bin'
		for file in os.listdir(path):
			d = fuzz.token_set_ratio(file, file_name)
			if d>=70:
				match = (path+ '/' + str(file))
				subprocess.Popen(match)
				speech_text = '%s running on Device'%file_name
	elif os.name == "nt":
		path = get_path()
		for drive in path:
			for root, dirs, files in os.walk(drive):
				for file in files:
					if file.endswith('.exe'):
						d = fuzz.token_set_ratio(file,file_name)
						if d >= 80:
							matches = (root + '/' + str(file))
							subprocess.Popen(matches)
							speech_text = 'file running %s'%file_name
	if speech_text == None :
		speech_text = "Unable to find requested file."
	return question(speech_text)


@ask.intent('phone_buzz')
def call_my_phone(phone_name):
	dialog_state = get_dialog_state()
	if dialog_state != 'COMPLETED':
		return delegate()
	for values in names():
		if values.lower() == phone_name.lower():
			speech_text = "Calling %s Now."%phone_name
			client.calls.create(to=calllist[values], from_=TWILIO_PHONE_NUMBER,url=WIML_INSTRUCTIONS_URL, method="GET")
	return question(speech_text)


@ask.intent('system_information')
def disp_sys_info():
	speech_text = "Running on %s in version %s on processor %s"%(platform.platform(),platform.machine(),platform.processor())
	return question(speech_text)
	

@ask.intent('open_webpage')
def open_web(webpage):
	dialog_state = get_dialog_state()
	if dialog_state != 'COMPLETED':
		return delegate()
	speech_text = None
	for values in pages():
		if values.lower() == webpage.lower():
			webbrowser.open(pagelist[values])
			speech_text = "Opened %s on your default browser"%webpage
	if speech_text == None :
		speech_text = "The web page's url is not found"
	return question(speech_text)	


@ask.intent('exit_session')
def session_ended():
    return statement("Ghost Busted.\n See You Next Time")


if __name__ == '__main__':
	if 'ASK_VERIFY_REQUESTS' in os.environ:
		verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
		if verify == 'false':
			app.config['ASK_VERIFY_REQUESTS'] = False
app.run(debug=True, port=5001)
