import os
import time
import requests
from bs4 import BeautifulSoup

page_range = [2, 12]

while page_range[0] < page_range[1]:
	try:
		page = page_range[0]
		page_link = 'https://github.com/MSWorkers/support.996.ICU/pulls?q=is%3Apr+is%3Aclosed&page=' + str(page)
		#print(page_link)
		r = requests.get(page_link)
		soup = BeautifulSoup(r.text, 'html.parser')
		results = soup.select("span.opened-by a")
		for res in results:
			user = res.text
			#print('user: %s' % user)
			user_link = 'https://github.com/' + str(user)
			r = requests.get(user_link)
			so = BeautifulSoup(r.text, 'html.parser')
			link = so.select('a[rel="nofollow me"]')
			if len(link) > 0:
				l = str(link[0].text) + '#' + str(user_link)
				print(l)
		page_range[0] += 1
	except (Exception, KeyboardInterrupt):
		print('Ctrl-C interrupt, enter to continue ...')
		inp = input()
		if inp == 'quit':
			quit();
		else:
			continue
