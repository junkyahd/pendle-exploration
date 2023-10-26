from __future__ import unicode_literals

AUTHOR = 'junkyahd'
AUTHOREMAIL = 'UnestablishedOrder@proton.me'
SITENAME = u'Chaos Champion'
# SITEURL = 'https://chaoschampion.website'
SITEURL = 'http://localhost:8000'

PATH = 'content'

THEME = 'C:/Users/jboersma/pelican-themes/graymill'


TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'en'

SITEDESCRIPTION = 'it is what it is'
DISPLAY_SUMMARY = False
DISPLAY_PAGES_ON_MENU = True

MENUITEMS = (('Home', SITEURL),
             )

# Feed generation is usually not desired when developing
FEED_ALL_RSS = False
FEED_ALL_ATOM = False
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

FAVICON = 'static/images/icons/rss.png'

STATIC_PATHS = ['images']
EXTRA_PATH_METADATA = {
    'extras/.htaccess': {'path': '.htaccess'},
    'extras/robots.txt': {'path': 'robots.txt'},
}


# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),
         ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
         ('You can modify those links in your config file', '#'),)


TWITTER_USERNAME = 'junkyahd'

# Social widget
SOCIAL = (
          ('github', 'https://github.com/junkyahd'),
          ('twitter', 'https://twitter.com/junkyahd'),
          )

DEFAULT_PAGINATION = 8

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True