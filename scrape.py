import requests, re, json
from bs4 import BeautifulSoup
from time import sleep

root_url = 'http://www.pmlp.gov.lv/lv/sakums/statistika/personvardu-datu-baze/?id=137' 
# FIXME hardkodētais id=137 nāk no http://www.pmlp.gov.lv/lv/sakums/statistika/personvardu-datu-baze redzamās formas ID parametra - varbūt tā viņiem ir datu versija? 

letters = 'abcčdefgģhijkķlļmnņoprsštuvzž'

data = {}

for letter in letters:
	query = '{}&query={}'.format(root_url, letter)
	r = requests.get(query)
	soup = BeautifulSoup(r.text, 'html.parser')

	last = soup.find('a', string='Pēdējā lapa')
	pages = int(re.search('page=([0-9]+)"', str(last)).group(1))

	print('Processing {} pages of "{}"...'.format(pages, letter))

	for page in range(1, pages+1):
		if page % 10 == 0:
			print('.', end='')
		if page % 100 == 0:
			print()
		# sleep(0.2) # limit to req/sec
		query = '{}&query={}&page={}'.format(root_url, letter, page)
		r = requests.get(query)
		soup = BeautifulSoup(r.text, 'html.parser')
		table = soup.find(id='firstnames-search-results')
		for row in table.findAll("tr"):
		    cells = row.findAll("td")
		    if len(cells) == 3:
		        name = cells[0].find(text=True)
		        number = cells[1].find(text=True)
		        data[name] = number

	with open("{}.json".format(letter), 'w', encoding = 'utf8') as outfile:
		json.dump(data, outfile, indent = 4, ensure_ascii=False)

	print('Processing "{}" done'.format(letter))

