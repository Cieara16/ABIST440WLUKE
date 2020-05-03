#!/bin/bash
# Deployment script
GIT_REPO = https://github.com/Cieara16/ABIST440WLUKE.git

pip install requests
pip install RPi.GPIO
pip install adafruit_CharLCD
PI_NAME = $(hostname)
git clone $GIT_REPO
cd ABIST440WLUKE

if [PI_NAME = 'PrepPi']
then
	python PrepTeamCopy11.py
fi

if [PI_NAME = 'MashPi']
then
	python Mashing_Team.py
fi

if [PI_NAME = 'BoilPi']
then
	python Boiling.py
fi

if [PI_NAME = 'FermentPi']
then
	python Fermenting.py
fi

if [PI_NAME = 'BottlePi']
then
	python BottleTeam_Final.py
fi

if [PI_NAME = 'ClosePi']
then
	sudo apt-get install -y cups
	sudo apt-get install -y hplip
	sudo usermod -a -G lpadmin pi
	sensible-browser 127.0.0.1:631/admin
	echo Add the printer through the gui. Elevation may be required.
	echo When finished, hit enter.
	read someline
	python PrepTeamCopy11.py
fi