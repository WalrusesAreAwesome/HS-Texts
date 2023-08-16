import json
from bs4 import BeautifulSoup
import re
import random
import math

# TODO PCG (among others) is counted as "other" rather than CG. I dont want to add 24*4 (P,C,F,?) aliases to EACH list
cs = "john, rose, dave, jade, aradia, tavros, sollux, karkat, nepeta, kanaya, terezi, vriska, equius, gamzee, eridan, feferi, aranea, meenah, jane, jake, roxy, dirk, calliope, caliborn, jasprosesprite^2, davepetasprite^2, other"
characterData = {}
for c in cs.split(", "):
	characterData[c.upper()] = {"lines": [], "wordCounts": {}, "cursePercentage": 0, "words": 0}

pre_scratch_alias = {
	"EB":"JOHN",
	"GT":"JOHN",
	"TT":"ROSE",
	"TG":"DAVE",
	"GG":"JADE",
	"AA":"ARADIA",
	"AT":"TAVROS",
	"TA":"SOLLUX",
	"CG":"KARKAT",
	"AC":"NEPETA",
	"GA":"KANAYA",
	"GC":"TEREZI",
	"AG":"VRISKA",
	"CT":"EQUIUS",
	"TC":"GAMZEE",
	"CA":"ERIDAN",
	"CC":"FEFERI"
}

post_scratch_alias = {
	"GT":"JAKE",
	"TT":"DIRK",
	"TG":"ROXY",
	"GG":"JANE",
	"AA":"ARADIA",
	"AT":"TAVROS",
	"TA":"SOLLUX",
	"CG":"KARKAT",
	"AC":"NEPETA",
	"GA":"KANAYA",
	"GC":"TEREZI",
	"AG":"ARANEA",
	"CT":"EQUIUS",
	"TC":"GAMZEE",
	"CA":"ERIDAN",
	"CC":"FEFERI",
	"UU":"CALLIOPE",
	"uu":"CALIBORN"
}

aliases = {}
def unquirk(character, text):
	if character == "ARADIA":
		text = re.sub("0", "o", text)
	elif character == "SOLLUX":
		text = re.sub("ii", "i", text)
		text = re.sub("2", "s", text)
	elif character == "NEPETA":
		text = re.sub("33", "ee", text)
	elif character == "TEREZI":
		text = re.sub("4", "a", text)
		text = re.sub("1", "i", text)
		text = re.sub("3", "e", text)
	elif character == "VRISKA":
		text = re.sub("8", "b", text) # NOT SO BUT IT'S NP COMPLETE
	elif character == "EQUIUS":
		text = re.sub("100", "loo", text)
		text = re.sub("%", "x", text)
	elif character == "ERIDAN":
		text = re.sub("vv", "v", text)
		text = re.sub("ww", "w", text)
	elif character == "FEFERI":
		text = re.sub("-+e", "e", text)
	return text


def createPureText():
	with open("mspa.json", "r") as f:
		data = json.load(f)

	with open("Pure_Text", "w") as f:
		for i in range(8130):
			page = str(i+1901).zfill(6)
			try:	
				text = data["story"][page]["content"]
				for l in text.split("<br />"):
					soup = BeautifulSoup(l, 'html.parser').get_text()
					f.write(soup + "\n")
			except:
				continue
			if i%813 == 0:
				print("{}%".format(i/813*10))

def charFill():
	with open("Pure_Text", "r") as f:
		text = f.read()
		lines = text.split("\n")
		for i,line in enumerate(lines):
			words = re.findall("[\w'\^]+", line)
			if len(words) > 0:
				try: # try: speaker = first word
					name = words[0]
					speaker = characterData[name]
				except:
					if i <= 32406:
						alias = pre_scratch_alias
					else:
						alias = post_scratch_alias
					try: # try: speaker is under alias (CG, AA, etc.)
						name = alias[words[0]]
						speaker = characterData[name]
					except:
						if len(words[0]) == 3 and words[0].upper() == words[0]: # if the first word is uppercase and 3 letters
							try:
								name = alias[words[0][1::]]
								speaker = characterData[name]
								print(words[0][1::])
							except:
								name = "OTHER"
						else:
							name = "OTHER" # others: narration, nannasprite, pipefan413
				characterData[name]["lines"].append(words)
		

		for c in characterData:
			print(c)
			swearCount = 0
			words = 0
			for l in characterData[c]["lines"]:
				if c != "OTHER":
					line = l[1::]
				else:
					line = l
				for w in line:

					try: # add to word counts
						characterData[c]["wordCounts"][w] += 1
					except:
						characterData[c]["wordCounts"][w] = 1

					swears = ["fuck", "shit", "ass", "dick", "damn", "bitch", "hell"]
					for s in swears:
						if len(re.findall(s, unquirk(c, w.lower()))) != 0:
							swearCount += 1

					characterData[c]["words"] += 1 # add to word count

			characterData[c]["cursePercentage"] = swearCount/characterData[c]["words"]
		print()



def sortByFactor():
	for c in dict(sorted(characterData.items(), key=lambda item: len(item[1]["wordCounts"]), reverse = True)):
		print("{}: {:.5f}".format(c, len(characterData[c]["wordCounts"])))

		"""
		wordsArray = re.findall("[\w']+", text)
		for word in wordsArray:
			word = word.lower()
			if random.random()*1000 < 1:
				print(word)
		"""

def findTrollNames():
	with open("Pure_Text", "r") as f:
		text = f.read()
	with open("Troll_Names", "w") as f:
		words = re.findall("[\w'\^]+", text)
		allWords = set()
		notUniqueWords = set()
		print(len(words))
		for i,w in enumerate(words):
			word = w.lower()
			if len({word}.intersection(allWords)) == 1:
				notUniqueWords.add(word)
			else:
				allWords.add(word)
			if i%6833 == 0:
				print("{:.0f}%, {}".format(i/6833, len(allWords)/len(notUniqueWords)))
		for word in allWords:
			f.write("{word}\n".format(word))

#createPureText()
#charFill()
#sortByFactor()
findTrollNames()
"""
with open("mspa.json", "r") as f:
	data = json.load(f)
text = data["story"]["008227"]["content"]
for l in text.split("<br />"):
	soup = BeautifulSoup(l, 'html.parser').get_text()
	print(soup)
"""






