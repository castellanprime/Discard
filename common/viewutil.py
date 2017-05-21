"""
	This module contains util functions, ie functions that have 
	no place in either of the modules in the directory. Right now, it
	is used to house code to render the game information as html
"""

def pretty_help():
	
	PATH='assets/doc/rules.md'

	from grip import serve
	import subprocess

	if self._internet_on():
		serve(path=PATH, user_content=True, browser=True)
	else:
		chrome_path = subprocess.check_output(['command', '-v', 'google-chrome'])
		subprocess.call([chrome_path, 'assets/doc/rules.html'])

def _internet_on():
	import socket
	from urllib.request import urlopen, Request
	from urllib.error import URLError

	timeout = 10
	socket.setdefaulttimeout(timeout)

	try:
		req = Request("https://www.google.com")
		urlopen(req)
		return True
	except URLError as err:
		print(err.reason)
		return False

