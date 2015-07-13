import mf2py
from string import Template

from xml.sax.saxutils import escape

TITLE_TEMPLATE = Template('<${t_type}>${title}</${t_type}>')

LINK_TEMPLATE = Template('<link href="${url}" rel="${rel}"></link>')

DATE_TEMPLATE = Template('<${dt_type}>${date}</${dt_type}>')

ID_TEMPLATE = Template('<id>${uid}</id>')

AUTHOR_TEMPLATE = Template('<author><name>${name}</name></author>')

FEATURED_TEMPLATE = Template('&lt;img src="${featured}"/&gt;')

POST_SUMMARY_TEMPLATE = Template('&lt;p&gt;${post_summary}&lt;/p&gt;')

MORELINK_TEMPLATE = Template('&lt;span&gt;Full article: &lt;a href="${url}"&gt;${name}&lt;/a&gt;&lt;/span&gt;')

SUMMARY_TEMPLATE = Template('<summary type="html">${featured}${summary}${morelink}</summary>')

CATEGORY_TEMPLATE = Template('<category term="${category}"></category>')

ENTRY_TEMPLATE = Template('<entry>${title}${link}${uid}${published}${updated}${summary}${categories}</entry>')

FEED_TEMPLATE = Template('<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en-us">${title}${subtitle}${link}${uid}${updated}${author}${entries}</feed>')

def updated_or_published(mf):
	"""
	get the updated date or the published date

	Args:
		mf: python dictionary of some object

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

def get_id(mf):
	"""
	get the uid of the mf object

	Args:
		mf: python dictionary of some object

	Return: string containing the uid property, or the url property or None

	"""

	props =  mf['properties']

	if 'uid' in props:
		return props['uid'][0]
	elif 'url' in props:
		return props['url'][0]
	else:
		return None


def entry2atom(entry_mf):
	"""
	convert microformats of a h-entry object to Atom 1.0

	Args:
		entry_mf: python dictionary of parsed microformats of a h-entry

	Return: an Atom 1.0 XML version of the microformats
	"""

	# be strict in requiring various properties to exist?
	props =  entry_mf['properties']

	# <entry>${title}${link}${uid}${published}${updated}{$summary}${categories}</entry>'
	entry = {'title':'', 'link':'', 'uid':'', 'published':'', 'updated':'', 'summary':'', 'categories':''}

	# construct title of entry
	name = escape(props['name'][0])
	entry['title'] = TITLE_TEMPLATE.substitute(title = name, t_type='title')

	# construct link/id of entry
	uid = escape(get_id(entry_mf))

	entry['link'] = LINK_TEMPLATE.substitute(url = uid, rel='alternate')

	# construct id of entry
	entry['uid'] = ID_TEMPLATE.substitute(uid = uid)

	# construct published date of entry
	entry['published'] = DATE_TEMPLATE.substitute(date = escape(props['published'][0]), dt_type = 'published')

	# construct updated/published date of entry
	updated = escape(updated_or_published(entry_mf))

	if updated is not None :
		entry['updated'] = DATE_TEMPLATE.substitute(date = updated, dt_type = 'updated')

	# construct summary of entry

	if 'featured' in props:
		featured = FEATURED_TEMPLATE.substitute(featured = escape(props['featured'][0]))

	if 'summary' in props:
		summary = POST_SUMMARY_TEMPLATE.substitute(post_summary = escape(props['summary'][0]))

	morelink =  MORELINK_TEMPLATE.substitute(url = uid, name = name)

	entry['summary'] = SUMMARY_TEMPLATE.substitute(featured=featured, summary=summary, morelink=morelink)

	# construct category list of entry
	if 'category' in props:
		for category in props['category']:
			entry['categories'] += CATEGORY_TEMPLATE.substitute(category=escape(category))

	# construct atom of entry

	return ENTRY_TEMPLATE.substitute(entry)


def hfeed2atom(doc=None, url=None):
	"""
	convert first h-feed object in a document to Atom 1.0

	Args:
		doc (file or string or BeautifulSoup doc): file handle, text of content
        to parse, or BeautifulSoup document to look for h-feed

	Return: an Atom 1.0 XML document version of the first h-feed in the document or None if no h-feed found
	"""

	# parse for microformats
	parsed = mf2py.Parser(doc, url).to_dict()

	# find first h-feed object if any or None
	try:
		mf = next(x for x in parsed['items'] if 'h-feed' in x['type'])
	except (KeyError, StopIteration):
		mf = None
		pass

	if mf is None:
		return None

	feed = {'title':'', 'subtitle':'', 'link':'', 'uid':'', 'updated':'', 'author':'', 'entries':''}

	props = mf['properties']

	# entries sorted by updated/published in reverse-chronology
	entries = sorted([x for x in mf['children'] if 'h-entry' in x['type']], key = lambda x: updated_or_published(x), reverse=True)

	# construct title for feed
	feed['title'] = TITLE_TEMPLATE.substitute(title = escape(props['name'][0]), t_type='title')

	# construct subtitle for feed
	feed['subtitle'] = TITLE_TEMPLATE.substitute(title = escape(props['additional-name'][0]), t_type='subtitle')

	uid = escape(get_id(mf))

	feed['link'] = LINK_TEMPLATE.substitute(url = uid, rel='alternate')

	# construct id of feed
	feed['uid'] = ID_TEMPLATE.substitute(uid = uid)

	# construct updated for feed or use updated of first post in entries
	feed['updated'] = DATE_TEMPLATE.substitute(date = escape(updated_or_published(mf) or updated_or_published(entries[0])), dt_type='updated' )

	# construct author for feed
	author = AUTHOR_TEMPLATE.substitute(name = escape(props['author'][0]['properties']['name'][0]))

	# construct entries for feed
	for entry in entries:
		# construct entry template
		feed['entries'] += entry2atom(entry)

	return FEED_TEMPLATE.substitute(feed)
