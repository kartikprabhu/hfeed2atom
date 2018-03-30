from string import Template
from . import __about__

GENERATOR = Template("""<generator uri="${uri}" version="${version}">${name}</generator>""").substitute(uri = __about__.URL['self'], version = '.'.join(map(str, __about__.VERSION[0:3])) + ''.join(__about__.VERSION[3:]), name = __about__.NAME )

TITLE = Template("""<${t_type}>${title}</${t_type}>""")

LINK = Template("""<link href="${url}" rel="${rel}"></link>""")

DATE = Template("""<${dt_type}>${date}</${dt_type}>""")

ID = Template("""<id>${uid}</id>""")

AUTHOR = Template("""<author><name>${name}</name></author>""")

FEATURED = Template("""&lt;img src="${featured}"/&gt;""")

POST_SUMMARY = Template("""&lt;p&gt;${post_summary}&lt;/p&gt;""")

MORELINK = Template("""&lt;span&gt;Full post: &lt;a href="${url}"&gt;${name}&lt;/a&gt;&lt;/span&gt;""")

SUMMARY = Template("""<summary type="html">${featured}${summary}${morelink}</summary>""")

CONTENT = Template("""<content type="html">${content}</content>""")

CATEGORY = Template("""<category term="${category}"></category>""")

ENTRY = Template("""<entry>${title}${subtitle}${link}${uid}${published}${updated}${summary}${content}
${categories}</entry>""")

FEED = Template("""<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en-us">${generator}${title}${subtitle}${link}${self}${uid}${updated}${author}${entries}</feed>""")

