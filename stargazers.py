import os
import time
import requests
from bs4 import BeautifulSoup

page_range = [37, 100]
limit_cache_num = 20

list_collect = []
def open_in_browser():
	global list_collect
	tot = len(list_collect)
	for idx, link in enumerate(list_collect):
		print("[%d / %d] %s" % (idx, tot, link))
		os.system('chromium ' + link)
		time.sleep(1)
	list_collect = []

while page_range[0] < page_range[1]:
	try:
		page = page_range[0]
		page_link = 'https://github.com/jupyter/notebook/stargazers?page=%d' % page
		print(page_link)
		r = requests.get(page_link)
		soup = BeautifulSoup(r.text, 'html.parser')
		results = soup.find_all("h3", "follow-list-name")
		for idx, res in enumerate(results):
			user = res.find('a')['href'].split('/')[1]
			print('page: %s, user: %s' % (page,user))
			user_link = 'https://github.com/' + str(user)
			r = requests.get(user_link)
			so = BeautifulSoup(r.text, 'html.parser')
			links = so.find_all('a', "u-url")
			for l in links:
				link = links[0].string
				if 'linkedin' in link:
					continue
				elif link == user_link:
					continue
				elif 'csdn' in link:
					continue
				elif 'twitter.com' in link:
					continue
				list_collect.append(str(link) + '#' + str(user_link))
				print(list_collect)
				print(len(list_collect))
				if len(list_collect) > limit_cache_num:
					raise Exception('overpage')
		page_range[0] += 1
	except (Exception, KeyboardInterrupt):
		print('Ctrl-C interrupt, enter to continue ...')
		inp = input()
		if inp == 'quit':
			quit();
		elif inp == 'open':
			open_in_browser()
open_in_browser()
