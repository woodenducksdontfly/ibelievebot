# NOTES
* I am using ports 8085 (a websocket that is used for audio) and 5000 (flask)
* I rely on python's single import functionality to create singletons of objects
* Setup is very manual at this time
* I use json files for data storage but should probably be using a lightweight db especially if this will join more than one channel

# TODO
* Flask Application can run in server
	* Create Flask GUI Control
		* Start Stop each thread
	* Create Flask GUI for Chat
		* Cache emotes
		* Receive messages from message inbox and display (apply emote htmls)
		* potential for MVC here where it determines how to control the ui with a controller
* Main app statup
    * args - mock - no auto
    * create message inbox (queue)
* Youtube Bot Thread
* Slack Bot Thread
* Create authorize twitch api endpoint point

# To work in the env
```
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```
