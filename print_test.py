import subprocess

lprString = subprocess.Popen(["/usr/bin/lp", "-d HP_DeskJet_2130_series beer_label.png"])
