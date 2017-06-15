"""
	This module represents the 
	entry point to Discard(tm)
"""
import sys, os, logging
## Logging is needed

logger = logging.getLogger('')
logger.setLevel(logging.INFO)

fh = logging.FileHandler('run.log', 'w', 'utf-8')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('- %(name)s - %(levelname)-8s: %(message)s')

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


import controllers.cmdcontroller as CmdController
import views.cmdview as CmdView
import common.viewutil as ViewUtil
import sys

def main():
	try:
		controller = CmdController.Controller([CmdView, ViewUtil])
		controller.start_game()
	except (SystemExit, KeyboardInterrupt):
		logger.info("Closing app..")


if __name__ == '__main__':
	main()

