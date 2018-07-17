import os
import psutil

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
	
@ask.intent('access_file')
def access_fl(file_name):
	os.system('gedit "{0}"'.format(file_name))
	speech_text = 'file open %s'%file_name
	return question(speech_text)


@ask.intent('access_file')
def play_music():


@ask.intent('exit_session')
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True, port=5001)
