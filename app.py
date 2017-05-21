"""
	This module represents the 
	entry point to Discard(tm)
"""


import controllers.cmdcontroller as CmdController
import views.cmdview as CmdView
import common.viewutil as ViewUtil
import common.game as Game

def main():
	controller = CmdController([CmdView, ViewUtil], Game)
	controller.main()

if __name__ == '__main__':
	main()

