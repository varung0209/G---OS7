import os
import psutil
import webbrowser
import difflib
import math
<<<<<<< HEAD
=======
import vlc
>>>>>>> 82bec569bf498995662adf785a45fe5d5a85320d

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
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

	
		
def sectohour(secs):
    mm, ss = divmod(secs, 60) # function to convert from secs to hours
    hh, mm = divmod(mm, 60)
    hh1 = int(math.fabs(hh))
    return (hh1, mm, ss)
   
  
@ask.intent('retrieve_timeleft')
def ret_timeleft():
	battery = psutil.sensors_battery()
	(hh, mm, ss) = sectohour(battery.secsleft)
	speech_text = 'time left is %s hour %s minutes'%(hh, mm)
	return question(speech_text)
	
	
@ask.intent('charge_status') # to check if laptop is put on charge or not
def ret_plugstatus():
	battery = psutil.sensors_battery()
	if(battery.power_plugged == True):
		speech_text = 'yes your laptop is on charge'
	else:
		speech_text = 'no your laptop is not on charge'
	return question(speech_text)
	
	
@ask.intent('access_file')
def accessfile(file_name):
<<<<<<< HEAD
	dialog_state = get_dialog_state()
	if dialog_state != 'COMPLETED':
		return delegate()
=======
>>>>>>> 82bec569bf498995662adf785a45fe5d5a85320d
	os.system('gedit "{0}"'.format(file_name))
	speech_text = 'file open %s'%file_name
	return question(speech_text)


@ask.intent('play_file')
<<<<<<< HEAD
def play_music(file_type,file_name):
	dialog_state = get_dialog_state()
	if dialog_state != 'COMPLETED':
		return delegate()
	if file_type == 'song' or file_type == 'music':
		path = '/home/purva'
		dir_path = os.path.dirname(path)
		for root, dirs, files in os.walk(dir_path):
			for file in files:
				if file.endswith('.mp3'):
					d = fuzz.token_set_ratio(file, file_name)
					if d>=80:
						matches=(root + '/'+str(file))
						speech_text = 'Playing on System'
						webbrowser.open(matches)
					else:
						speech_text = 'Unable to find file'
		return question(speech_text)
	if file_type == 'video' or file_type == 'movie':
		path = '/home/purva'
		dir_path = os.path.dirname(path)
		for root, dirs, files in os.walk(dir_path):
			for file in files:
				if file.endswith('.mp4'):
					d = fuzz.token_set_ratio(file, file_name)
					if d>=80:
						matches=(root + '/'+str(file))
						speech_text = 'Playing on System'
						webbrowser.open(matches)
					else:
						speech_text = 'Unable to find file'
		return question(speech_text)
		
#@ask.intent('execute_file')
#def execute_file(file_name):
	#os.system(start 'C:\pathtotool.exe -2 c:\data')
	#speech_text = 'file running %s'%file_name
	#return question(speech_text)
=======
def play_music(file_name):
	to_search = file_name + '.mp3'
	path = '/home/purva/videos'
	for filename in os.listdir(path):
		d = difflib.SequenceMatcher(None, filename, to_search).ratio()
		if d>=0.6:
			matches=(os.path.join(path, filename))
	webbrowser.open(matches)
>>>>>>> 82bec569bf498995662adf785a45fe5d5a85320d

@ask.intent('phone_buzz')
def call_my_phone():
	speech_text = "Calling your Phone now"
	client.calls.create(to="+918147486031", from_=TWILIO_PHONE_NUMBER,url=WIML_INSTRUCTIONS_URL, method="GET")
	return question(speech_text)

@ask.intent('play_video') #intent name
def play_vdieo(file_name):
	to_search = file_name + '.mp4'
	path = '/home/purva/videos'
	for filename in os.listdir(path):
		d = difflib.SequenceMatcher(None, filename, to_search).ratio()
		if d>=0.6:
			matches=(os.path.join(path, filename))
	webbrowser.open(matches)
	

@ask.intent('') # intent name
def execute_file(file_name):
	os.system(start 'C:\pathtotool.exe -2 c:\data')
	speech_text = 'file running %s'%file_name
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
