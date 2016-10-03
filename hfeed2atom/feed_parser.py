import requests
from bs4 import BeautifulSoup

import mf2py
import mf2util



def feed_parser(doc=None, url=None):
	"""
	parser to get hfeed
	"""

	if doc:
		if not isinstance(doc, BeautifulSoup):
			doc = BeautifulSoup(doc)

	if url:
		if doc is None:
			data = requests.get(url)

			# check for charater encodings and use 'correct' data
			if 'charset' in data.headers.get('content-type', ''):
				doc = BeautifulSoup(data.text)
			else:
				doc = BeautifulSoup(data.content)

	# find first h-feed object if any or construct it

	hfeed = doc.find(class_="h-feed")

	if hfeed:
		hfeed = mf2py.Parser(hfeed, url).to_dict()['items'][0]
	else:
		hfeed = {'type': ['h-feed'], 'properties': {}, 'children': []}

		# parse whole document for microformats
		parsed = mf2py.Parser(doc, url).to_dict()

		# construct h-entries from top-level items
		hfeed['children'] = [x for x in parsed['items'] if 'h-entry' in x.get('type', [])]


	# construct fall back properties for hfeed

	props = hfeed['properties']

	# if no name or name is the content value, construct name from title or default from URL
	name = props.get('name')
	if name:
		name = name[0]

	content = props.get('content')
	if content:
		content = content[0]
		if isinstance(content, dict):
			content = content.get('value')

	if not name or not mf2util.is_name_a_title(name, content):
		feed_title = doc.find('title')
		if feed_title:
			hfeed['properties']['name'] = [feed_title.get_text()]
		elif url:
			hfeed['properties']['name'] = ['Feed for' + url]

	# construct author from rep_hcard or meta-author

	# construct uid from url
	if 'uid' not in props and 'url' not in props:
		if url:
			hfeed['properties']['uid'] = [url]

	# construct categories from meta-keywords
	if 'category' not in props:
		keywords = doc.find('meta', attrs= {'name': 'keywords', 'content': True})
		if keywords:
			hfeed['properties']['category'] = keywords.get('content', '').split(',')


	return hfeed
