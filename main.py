import os
import psutil
import webbrowser
import difflib
import math
import vlc

from flask import Flask
from flask_ask import Ask, question, statement

app = Flask(__name__)
ask = Ask(app, "/")
re_enter = 'Anythin else I can do for you?'


@ask.launch
def launch():
    speech_text = 'Launching Protocol'
    return question(speech_text)


@ask.intent('retrieve_percentage')
def ret_battery():
	battery = psutil.sensors_battery()
	speech_text = 'battery percentage is %s'%battery.percent
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
	os.system('gedit "{0}"'.format(file_name))
	speech_text = 'file open %s'%file_name
	return question(speech_text)


@ask.intent('play_file')
def play_music(file_name):
	to_search = file_name + '.mp3'
	path = '/home/purva/videos'
	for filename in os.listdir(path):
		d = difflib.SequenceMatcher(None, filename, to_search).ratio()
		if d>=0.6:
			matches=(os.path.join(path, filename))
	webbrowser.open(matches)


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
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True, port=5001)
