import json, re
from collections import defaultdict

freqs = defaultdict(int)
with open("ž.json", 'r', encoding = 'utf8') as file:
	data = json.load(file)
	for name, count in data.items():
		for element in name.split(' '):
			freqs[element.capitalize()] += int(count)

print(len(freqs))
for name, count in sorted(freqs.items(), key=lambda x:x[1], reverse=True):
	# print(name, count)
	pass


lexicon = '/Users/pet/Documents/java_ws/morphology/src/main/resources/Lexicon_firstnames.xml'
lexicon_new = '/Users/pet/Documents/java_ws/morphology/src/main/resources/Lexicon_firstnames_freqs.xml'
with open(lexicon, 'r', encoding = 'utf8') as in_file:
	with open(lexicon_new, 'w', encoding='utf8') as out_file:
		for line in in_file.readlines():
			match = re.search('Pamatforma="(.*)"/></Lexeme>', line)
			if match:
				name = match.group(1)	
				freq = freqs.get(name)
				line = line.replace('"/></Lexeme>', '" Biežums="{}"/></Lexeme>'.format(freq))
			out_file.write(line)
