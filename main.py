import os
import psutil
import webbrowser
import difflib
import math

from flask import Flask
from flask_ask import Ask, question, statement

app = Flask(__name__)
ask = Ask(app, "/")


@ask.launch
def launch():
    speech_text = 'Launching Protocol'
    return question(speech_text)


def sectohour(secs):
    mm, ss = divmod(secs, 60) # function to convert from secs to hours
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
	os.system('gedit "{0}"'.format(file_name))
	speech_text = 'file open %s'%file_name
	return question(speech_text)


@ask.intent('play_file')
def play_music(file_type,file_name):
	if file_type == 'song':
		to_search = file_name + '.mp3'
		path = '/home/archeon/Music'
		for filename in os.listdir(path):
			d = difflib.SequenceMatcher(None, filename, to_search).ratio()
			if d>=0.6:
				matches=(os.path.join(path, filename))
				speech_text = 'Playing on System'
				webbrowser.open(matches)
			else :
				speech_text = 'Unable to find file'
		return question(speech_text)
	if file_type == 'video':
		to_search = file_name + '.mp4'
		path = '/home/archeon/Videos'
		for filename in os.listdir(path):
			d = difflib.SequenceMatcher(None, filename, to_search).ratio()
			if d>=0.6:
				matches=(os.path.join(path, filename))
				speech_text = 'Playing on System'
				webbrowser.open(matches)
			else :
				speech_text = 'Unable to find file'
		return question(speech_text)


#@ask.intent('execute_file')
#def execute_file(file_name):
	#os.system(start 'C:\pathtotool.exe -2 c:\data')
	#speech_text = 'file running %s'%file_name
	#return question(speech_text)


@ask.intent('exit_session')
def session_ended():
    return statement("Session ended")


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True, port=5001)
