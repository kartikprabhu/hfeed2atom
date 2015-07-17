import mf2py
from bs4 import BeautifulSoup

def feed_parser(doc=None, url=None):
	"""
	parser to get hfeed
	"""

	if not isinstance(doc, BeautifulSoup):
		doc = BeautifulSoup(doc)

	# parse for microformats
	parsed = mf2py.Parser(doc, url).to_dict()

	# find first h-feed object if any or construct it
	try:
		hfeed = next(x for x in parsed['items'] if 'h-feed' in x.get('type', []))
	except (KeyError, StopIteration):
		hfeed = {'type': ['h-feed'], 'properties': {}, 'children': []}

		# construct name from title
		title = doc.find('title')
		if title:
			hfeed['properties']['name'] = [title.get_text()]

		# construct author from rep_hcard or meta-author

		# construct uid from url
		if url:
			hfeed['properties']['uid'] = url

		# construct categories from meta-keywords
		keywords = doc.find('meta', attrs= {'name': 'keywords', 'content': True})['content']
		if keywords:
			hfeed['properties']['category'] = keywords.split(',')

		# construct entries
		hfeed['children'] = [x for x in parsed['items'] if 'h-entry' in x.get('type', [])]

		pass

	return hfeed

