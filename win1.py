import os
import psutil
import webbrowser
import math
import subprocess

from fuzzywuzzy import fuzz
from flask import Flask
from flask_ask import Ask, statement, question, delegate,session
from twilio.rest import TwilioRestClient

TWILIO_PHONE_NUMBER = "+18053358898"
WIML_INSTRUCTIONS_URL = "http://static.fullstackpython.com/phone-calls-python.xml"
client = TwilioRestClient("AC7b97a7a6264813fafd695f02b7b071a5", "4502047c06369e5aa4f1a436d0787c88")

app = Flask(__name__)
ask = Ask(app, "/")

def get_dialog_state():
	return session['dialogState']

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
	speech_text = 'Launching Protocol'
	return question(speech_text)


def sectohour(secs):
	mm, ss = divmod(secs, 60)
	hh, mm = divmod(mm, 60)
	hh1 = int(math.fabs(hh))
	return (hh1, mm, ss)


@ask.intent('retrieve_percentage')
def ret_battery():
	battery = psutil.sensors_battery()
	(hh, mm, ss) = sectohour(battery.secsleft)
	if(battery.power_plugged == True):
		speech_text = 'Battery Percentage is %s \n Time left is %s hour %s minutes \n Status : Charging'%(battery.percent,hh, mm)
	else:
		speech_text = 'Battery Percentage is %s \n Time left is %s hour %s minutes \n Status : Discharging'%(battery.percent,hh, mm)
	return question(speech_text)

	
@ask.intent('access_file')
def accessfile(file_name):
	dialog_state = get_dialog_state()
	if dialog_state != 'COMPLETED':
		return delegate()
	speech_text = None
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
	path = get_path()
	if file_type == 'song' or file_type == 'music':
		for root, dirs, files in os.walk(path):
			for file in files:
				file1 = file.replace(' ', '')
				if file1.endswith('.mp3'):
					d = fuzz.token_set_ratio(file1, file_name)
					if d>=80:
						matches=(root + '/'+str(file))
						speech_text = 'Playing on System'
						webbrowser.open(matches)
						return question(speech_text)
					else:
						speech_text = 'Unable to find file'
		return question(speech_text)
	if file_type == 'video' or file_type == 'movie':
		for root, dirs, files in os.walk(path):
			for file in files:
				file1 = file.replace(' ', '')
				if file1.endswith('.mp4'):
					d = fuzz.token_set_ratio(file1, file_name)
					if d>=80:
						matches=(root + '/'+str(file))
						speech_text = 'Playing on System'
						webbrowser.open(matches)
						return question(speech_text)
					else:
						speech_text = 'Unable to find file'
		return question(speech_text)
	
		
@ask.intent('execute_file')
def execute_file(file_name):
	path = get_path()
	for drive in path:
    		for root, dirs, files in os.walk(drive):
            		for file in files:
		       		if file.endswith('.exe'):
		        		d = fuzz.token_set_ratio(file, file_name)
		            		if d >= 80:
		                	matches = (root + '/' + str(file))
					subprocess.Popen(matches)
					speech_text = 'file running %s'%file_name
	return question(speech_text)


@ask.intent('phone_buzz')
def call_my_phone():
	speech_text = "Calling your Phone now"
	client.calls.create(to="+918147486031", from_=TWILIO_PHONE_NUMBER,url=WIML_INSTRUCTIONS_URL, method="GET")
	return question(speech_text)


@ask.intent('exit_session')
def session_ended():
    return statement("Session ended")


if __name__ == '__main__':
	if 'ASK_VERIFY_REQUESTS' in os.environ:
		verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
		if verify == 'false':
			app.config['ASK_VERIFY_REQUESTS'] = False
app.run(debug=True, port=5001)
