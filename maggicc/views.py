# -*- coding: utf-8 -*-

import logging

from itertools import ifilter
from itertools import imap
from itertools import islice
from itertools import groupby

from maggicc import app
from maggicc.core import publications

from flask import render_template
from flask import flash
from flask import escape
from flask import redirect
from flask import url_for
from flask import request
from flask import g
from flask import abort
from flask import session

from jinja2.exceptions import TemplateNotFound

def page(slug='', data={}):
    pages = app.config['PAGES']
    if slug in pages:
        try:
            return render_template(
                '%s.html' % slug,
                pages=pages,
                page=pages[slug],
                current=slug,
                data=data)
        except KeyError, e:
            logging.warning(e)
    return render_template('400.html')


@app.route('/research')
def view_research():
    return page('research')


@app.route('/')
def view_index():
    items = publications.parse_bibtex(app.config['PUBLICATIONS_DB'])
    items = imap(publications.publication_formatter,
        items)
    selected_publications = ifilter(publications.is_selected, items)
    selected_publications = islice(selected_publications, 3)

    return page('index', data={
        'selected_publications': list(selected_publications)})


@app.route('/talks/')
def view_talks():
    return page('talks')

@app.route('/publications/')
def view_publications():
    items = publications.parse_bibtex(
            app.config['PUBLICATIONS_DB'])
    items = sorted(imap(publications.publication_formatter,
        items), key=publications.publication_type)
    pub_list = dict(
            [(t,list(els)) \
                    for t,els in groupby(items, publications.publication_type)])

    return page('publications', data={
        'publications': pub_list,
        'types_order': app.config['PUBLICATIONS_TYPES_ORDER']})

