import os
import time
import requests
from bs4 import BeautifulSoup

page_range = [129, 159]
limit_cache_num = 25

list_collect = []
save_idx = 0
while page_range[0] < page_range[1]:
	try:
		page = page_range[0]
		page_link = 'https://github.com/programthink?page=%d&tab=followers' % page
		print(page_link)
		r = requests.get(page_link)
		soup = BeautifulSoup(r.text, 'html.parser')
		results = soup.find_all("span", "link-gray pl-1")
		for idx, res in enumerate(results):
			if idx < save_idx:
				continue
			save_idx = idx
			user = res.string
			print('page: %s, user: %s' % (page,user))
			user_link = 'https://github.com/' + str(user)
			r = requests.get(user_link)
			so = BeautifulSoup(r.text, 'html.parser')
			links = so.find_all('a', "u-url")
			for l in links:
				link = links[0].string
				list_collect.append(str(link) + '#' + str(user_link))
				print(list_collect)
				print(len(list_collect))
				if len(list_collect) > limit_cache_num:
					raise Exception('overpage')
		page_range[0] += 1
		save_idx = 0
	except (Exception, KeyboardInterrupt):
		print('Ctrl-C interrupt, enter to continue ...')
		inp = input()
		if inp == 'quit':
			quit();
		elif inp == 'open':
			tot = len(list_collect)
			for idx, link in enumerate(list_collect):
				print("[%d / %d]" % (idx, tot))
				os.system('chromium ' + link)
				time.sleep(1)
			list_collect = []
		else:
			print('starting from ' + str(save_idx))
			continue

tot = len(list_collect)
for idx, link in enumerate(list_collect):
	print("[%d / %d]" % (idx, tot))
	os.system('chromium ' + link)
	time.sleep(1)
