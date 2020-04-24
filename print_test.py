import subprocess
import datetime
#works for initial label printing
#subprocess.Popen(['/usr/bin/lp', '-d', 'HP_DeskJet_2130_series', '-o', 'orientation-requested=3', 'beer_label.png'])
#extracted label printing

current_date = datetime.now().tostring()
#text_for_label = 'text 190,490 "Cool Island Beer\n' + current_date + '\nABV: 8.3%\n15.5 Gal"'
text_for_label = 'text 190,490 "' + beer_name + ' ' + current_date + ' ABV: ' + abv + '% ' + keg_volume + ' Gal"'
subprocess.Popen(['/usr/bin/convert', '-pointsize', '18', '-draw', text_for_label, 'beer_label.png', 'beer_label_withtext.png'])
#subprocess.Popen(['/usr/bin/lp', '-d', 'HP_DeskJet_2130_series', '-o', 'orientation-requested=3', 'beer_label_withtext.png'])