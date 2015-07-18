from xml.sax.saxutils import escape
from string import Template

from . import about, feed_parser

GENERATOR = Template('<generator uri="${uri}" version="${version}">${name}</generator>').substitute(uri = about.URL['self'], version = '.'.join(map(str, about.VERSION[0:3])) + ''.join(about.VERSION[3:]), name = about.NAME )

TITLE_TEMPLATE = Template('<${t_type}>${title}</${t_type}>')

LINK_TEMPLATE = Template('<link href="${url}" rel="${rel}"></link>')

DATE_TEMPLATE = Template('<${dt_type}>${date}</${dt_type}>')

ID_TEMPLATE = Template('<id>${uid}</id>')

AUTHOR_TEMPLATE = Template('<author><name>${name}</name></author>')

FEATURED_TEMPLATE = Template('&lt;img src="${featured}"/&gt;')

POST_SUMMARY_TEMPLATE = Template('&lt;p&gt;${post_summary}&lt;/p&gt;')

MORELINK_TEMPLATE = Template('&lt;span&gt;Full article: &lt;a href="${url}"&gt;${name}&lt;/a&gt;&lt;/span&gt;')

SUMMARY_TEMPLATE = Template('<summary type="html">${featured}${summary}${morelink}</summary>')

CONTENT_TEMPLATE = Template('<content type="html">${content}</content>')

CATEGORY_TEMPLATE = Template('<category term="${category}"></category>')

ENTRY_TEMPLATE = Template('<entry>${title}${subtitle}${link}${uid}${published}${updated}${summary}${content}${categories}</entry>')

FEED_TEMPLATE = Template('<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en-us">${generator}${title}${subtitle}${link}${uid}${updated}${author}${entries}</feed>')

def _updated_or_published(mf):
	"""
	get the updated date or the published date

	Args:
		mf: python dictionary of some microformats object

	Return: string containing the updated date if it exists, or the published date if it exists or None

	"""

	props =  mf['properties']

	# construct updated/published date of mf
	if 'updated' in props:
		return props['updated'][0]
	elif 'published' in props:
		return props['published'][0]
	else:
		return None

def _get_id(mf, url=None):
	"""
	get the uid of the mf object

	Args:
		mf: python dictionary of some microformats object
		url: optional URL to use in case no uid or url in mf

	Return: string containing the id or None

	"""

	props =  mf['properties']

	if 'uid' in props:
		return props['uid'][0]
	elif 'url' in props:
		return props['url'][0]
	else:
		return None


def hentry2atom(entry_mf):
	"""
	convert microformats of a h-entry object to Atom 1.0

	Args:
		entry_mf: python dictionary of parsed microformats of a h-entry

	Return: an Atom 1.0 XML version of the microformats or None if error, and error message
	"""

	# generate fall backs or errors for the non-existing required properties ones.

	if 'properties' in entry_mf:
		props =  entry_mf['properties']
	else:
		return None, 'properties of entry not found.'

	entry = {'title': '', 'subtitle': '', 'link': '', 'uid': '', 'published': '', 'updated': '', 'summary': '', 'content': '',  'categories': ''}

	## required properties first

	# construct title of entry -- required - add default
	if 'name' in props:
		name = props['name'][0]
		entry['title'] = TITLE_TEMPLATE.substitute(title = escape(name), t_type='title')
	else:
		return None, 'title for entry not found'

	# construct id of entry
	uid = _get_id(entry_mf)

	if uid:
		# construct id of entry -- required
		entry['uid'] = ID_TEMPLATE.substitute(uid = escape(uid))
	else:
		return None, 'entry does not have a valid id'

	# construct updated/published date of entry
	updated = _updated_or_published(entry_mf)

	# updated is  -- required
	if updated:
		entry['updated'] = DATE_TEMPLATE.substitute(date = escape(updated), dt_type = 'updated')
	else:
		return None, 'entry does not have valid updated date'

	## optional properties

	entry['link'] = LINK_TEMPLATE.substitute(url = escape(uid), rel='alternate')

	# construct published date of entry
	if 'published' in props:
		entry['published'] = DATE_TEMPLATE.substitute(date = escape(props['published'][0]), dt_type = 'published')

	# construct subtitle for feed
	if 'additional-name' in props:
		feed['subtitle'] = TITLE_TEMPLATE.substitute(title = escape(props['additional-name'][0]), t_type='subtitle')

	# add content processing
	if 'content' in props:
		if isinstance(props['content'][0], dict):
			content = props['content'][0]['html']
		else:
			content = props['content'][0]
	else:
		content = None

	if content:
		entry['content'] = CONTENT_TEMPLATE.substitute(content = escape(content))

	# construct summary of entry
	if 'featured' in props:
		featured = FEATURED_TEMPLATE.substitute(featured = escape(props['featured'][0]))
	else:
		featured = ''

	if 'summary' in props:
		summary = POST_SUMMARY_TEMPLATE.substitute(post_summary = escape(props['summary'][0]))
	else:
		summary = ''

	# make morelink if content does not exist
	if not content:
		morelink =  MORELINK_TEMPLATE.substitute(url = escape(uid), name = escape(name))
	else:
		morelink = ''

	entry['summary'] = SUMMARY_TEMPLATE.substitute(featured=featured, summary=summary, morelink=morelink)

	# construct category list of entry
	if 'category' in props:
		for category in props['category']:
			entry['categories'] += CATEGORY_TEMPLATE.substitute(category=escape(category))

	# construct atom of entry
	return ENTRY_TEMPLATE.substitute(entry), 'up and Atom!'


def hfeed2atom(doc=None, url=None, hfeed=None):
	"""
	convert first h-feed object in a document to Atom 1.0

	Args:
		doc (file or string or BeautifulSoup doc): file handle, text of content
        to parse, or BeautifulSoup document to look for h-feed
		url: url of the document, used for making absolute URLs from url data, or for fetching the document

	Return: an Atom 1.0 XML document version of the first h-feed in the document or None if no h-feed found, and string with reason for error
	"""
	# if hfeed object given assume it is well formatted
	if hfeed:
		mf = hfeed
	else:
		# send to hfeed_parser to parse
		mf = feed_parser.feed_parser(doc, url)

		if not mf:
			return None, 'h-feed not found'

	feed = {'generator': '', 'title': '', 'subtitle': '', 'link': '', 'uid': '', 'updated': '', 'author': '', 'entries': ''}

	if 'properties' in mf:
		props = mf['properties']
	else:
		return None, 'h-feed properties not found.'

	## required properties first

	#construct title for feed -- required
	if 'name' in props:
		feed['title'] = TITLE_TEMPLATE.substitute(title = escape(props['name'][0]), t_type='title')
	else:
		return None, 'title for feed not found'

	uid = _get_id(mf) or url

	# id is -- required
	if uid:
		# construct id of feed -- required
		feed['uid'] = ID_TEMPLATE.substitute(uid = escape(uid))
	else:
		return None, 'feed does not have a valid id'

	# entries
	if 'children' in mf:
		entries = [x for x in mf['children'] if 'h-entry' in x['type']]
	else:
		entries = []

	# construct updated/published date of feed.
	updated = _updated_or_published(mf)

	if not updated and entries:
		updated = max([_updated_or_published(x) for x in entries])

	# updated is  -- required
	if updated:
		feed['updated'] = DATE_TEMPLATE.substitute(date = escape(updated), dt_type = 'updated')
	else:
		return None, 'updated date for feed not found, and could not be constructed from entries.'

	## optional properties

	# construct subtitle for feed
	if 'additional-name' in props:
		feed['subtitle'] = TITLE_TEMPLATE.substitute(title = escape(props['additional-name'][0]), t_type='subtitle')

	feed['link'] = LINK_TEMPLATE.substitute(url = escape(uid), rel='alternate')

	# construct author for feed
	if 'author' in props:
		author = AUTHOR_TEMPLATE.substitute(name = escape(props['author'][0]['properties']['name'][0]))

	# construct entries for feed
	for entry in entries:
		# construct entry template  - skip entry if error
		entry_atom, message = hentry2atom(entry)
		if entry_atom:
			feed['entries'] += entry_atom

	feed['generator'] = GENERATOR

	return FEED_TEMPLATE.substitute(feed), 'up and Atom!'
