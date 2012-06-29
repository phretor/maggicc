import io
import os
import sys
import glob
import string
import logging
import datetime

from operator import attrgetter
from operator import itemgetter

from itertools import imap

from pybtex.database import BibliographyData
from pybtex.database.input import bibtex
from pybtex.database.output import bibtex as bibtex_writer
from pybtex.backends.html import Backend as HTMLBackend
from pybtex.style.names import BaseNameStyle, name_part
from pybtex.style.template import join

from maggicc.settings import Config
config = Config()

from IPython import embed


class NameStyle(BaseNameStyle):
    name = 'flast'
    aliases = 'f_last'

    def format(self, person, abbr=False):
        return join [
            name_part(tie=True) [person.first(abbr) + person.middle(abbr)],
            name_part(tie=True) [person.prelast()],
            name_part [person.last()],
        ]


def publication_date(fields):
    if 'date' not in fields and 'year' in fields:
        fields['date'] = '%s-01-01' % fields['year']

    try:
        return datetime.datetime.strptime(fields['date'], '%Y-%m-%d')
    except Exception, e:
        logging.warning(e)
    return datetime.datetime.now()


def is_selected(publication):
    return 'keywords' in publication['data'].fields \
        and 'selected' in publication['data'].fields['keywords']


def sorter(item):
    item = item['data']
    return publication_date(item.fields)



def create_snippet(key, value):
    out = io.StringIO()
    bw = bibtex_writer.Writer()
    bw.write_stream(BibliographyData(entries={key: value}), out)
    out.seek(0)
    return out.read()


def attach_files(slug):
    files = glob.iglob(os.path.join(config.PUBLICATIONS_PATH, slug, '*.*'))
    files = imap(file_formatter, files)
    return files


def clean_filename(filename, allowed=None):
    if allowed is None or not isinstance(allowed, basestring):
        allowed = string.letters
    filename = ''.join([c for c in filename if c in allowed])
    return filename


def file_formatter(path):
    url = os.path.relpath(path, config.STATIC_PATH)
    title, extension = os.path.splitext(os.path.basename(path))
    title = clean_filename(title)
    extension = clean_filename(extension)
    return {'title': title, 'extension': extension, 'url': url}


def publication_formatter((slug, data)):
    return {
        'slug': slug,
        'data': data,
        'files': attach_files(slug),
        'snippet': create_snippet(slug, data) }


def publication_type(publication):
    t = publication['data'].type
    if t in config.PUBLICATIONS_TYPES:
        return config.PUBLICATIONS_TYPES[t]
    return config.PUBLICATIONS_TYPES['default'] 


def parse_bibtex(file_path):
    if os.path.isfile(file_path):
        parser = bibtex.Parser()
        return parser.parse_file(file_path).entries.iteritems()
    return {}.iteritems() #empty iterator
