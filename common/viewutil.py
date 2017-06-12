"""
	This module contains util functions, ie functions that have 
	no place in either of the modules in the directory. Right now, it
	is used to house code to render the game information as html
"""

def pretty_help():
	PATH = 'assets/doc/rules.html'
	
	import os, webbrowser
	try:
		from urllib import pathname2url         # Python 2.x
	except:
		from urllib.request import pathname2url # Python 3.x

	url = 'file:{}'.format(pathname2url(os.path.abspath(PATH)))
	webbrowser.open(url)

