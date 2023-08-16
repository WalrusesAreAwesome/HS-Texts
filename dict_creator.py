chars = "john, rose, dave, jade, aradia, tavros, sollux, karkat, nepeta, kanaya, terezi, vriska, equius, gamzee, eridan, feferi, aranea, meenah, jane, jake, roxy, dirk, calliope, caliborn, jasprosesprite^2, davepetasprite^2, other"
tags = "eb, tt, tg, gg, aa, at, ta, cg, ac, ga, gc, ag, ct, tc, ca, cc"
"""
for i,t in enumerate(tags.split(", ")):
	try:
		print('\t"{}":"{}",'.format(t.upper(), chars.split(", ")[i].upper()))
	except:
		print("end...")
"""

for c in chars.split(", "):
	print('\t"' + c.upper() + '": {"lines": [], "words": set(), "wordsCount": {}, "cursePercentage": 0},')