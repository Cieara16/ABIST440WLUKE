#!/bin/bash
# Deployment script
GIT_REPO="https://github.com/Cieara16/ABIST440WLUKE.git"
pip install requests
pip install RPi.GPIO
pip install adafruit_CharLCD
PI_NAME=$(hostname)
git clone $GIT_REPO
cd ABIST440WLUKE

case $PI_NAME in

	"PrepPi")
		python PrepTeamCopy11.py;;
	"MashPi")
		python Mashing_Team.py;;
	"BoilPi")
		python BoilPhase.py;;
	"FermentPi")
		python Fermenting.py;;

	"BottlePi")
		python BottleTeam_Final.py;;
	"ClosePi")
		sudo apt-get install -y cups
		sudo apt-get install -y hplip
		sudo usermod -a -G lpadmin pi
		sensible-browser 127.0.0.1:631/admin
		echo Add the printer through the gui. Elevation may be required.
		echo When finished, hit enter.
		read someline
		python ClosePi.py;;
esac