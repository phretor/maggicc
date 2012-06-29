import jinja2
from flask import Flask

from maggicc.settings import Config

#registering filters
from maggicc.filters import format_author
from maggicc.filters import publication_sorter
from maggicc.filters import publication_venue
from maggicc.filters import publication_where
from maggicc.filters import publication_date

jinja2.filters.FILTERS['format_author'] = format_author
jinja2.filters.FILTERS['publication_sorter'] = publication_sorter
jinja2.filters.FILTERS['publication_venue'] = publication_venue
jinja2.filters.FILTERS['publication_where'] = publication_where
jinja2.filters.FILTERS['publication_date'] = publication_date

#starting the app
app = Flask(__name__)
app.config.from_object(Config())

import maggicc.views
