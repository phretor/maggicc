import datetime

from maggicc.core.publications import NameStyle
from maggicc.core.publications import sorter
from maggicc.core.publications import publication_date as publication_datetime

from pybtex.backends.html import Backend

def format_author(person):
    flast = NameStyle().format
    return flast(person, abbr=True).format().render(Backend())

def publication_sorter(publication_list):
    return iter(sorted(publication_list, key=sorter, reverse=True))

def publication_date(fields):
    return publication_datetime(fields).strftime('%d/%m/%Y')

def publication_venue(fields):
    if 'venue' in fields:
        return fields['venue']

    if 'address' in fields:
        return fields['address']

    return 'Unknown'

def publication_where(fields):
    if 'journal' in fields:
        return fields['journal']

    if 'booktitle' in fields:
        return fields['booktitle']

    return 'Unknown'
