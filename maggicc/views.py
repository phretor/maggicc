# -*- coding: utf-8 -*-

import logging
import os
import codecs

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


# helpers
def pages():
    return app.config['PAGES']


def page404():
    return render_template(
            '400.html',
            page={'title': 'Not found'},
            pages=pages())


def page(slug='', data={}, template=None, title=''):
    pages_list = pages()

    if slug in pages_list and template is None:
        page = pages_list[slug]
        template = '%s.html' % slug
    else:
        page = {'title': title}

    try:
        return render_template(
            template,
            pages=pages_list,
            page=page,
            current=slug,
            data=data)
    except KeyError, e:
        logging.warning(e)

    return page404()


dirs = lambda p:filter(lambda x:os.path.isdir(os.path.join(p, x)), os.listdir(p))


def courses():
    path = os.path.join(app.config['TEMPLATES_PATH'], 'teaching', 'detail')
    course_list = {}

    for course in dirs(path):
        title = codecs.open(
                os.path.join(path, course, 'title.html'),
                encoding='utf-8').read().strip()
        desc = codecs.open(
                os.path.join(path, course, 'description.html'),
                encoding='utf-8').read().strip()

        course_list[course] = {
                'desc': desc,
                'title': title,
                'editions': {}
                }

        _path = os.path.join(path, course)

        for year in dirs(_path):
            org = codecs.open(
                    os.path.join(_path, year, 'org.html'),
                    encoding='utf-8').read().strip()
            lang = 'ita'
            if os.path.isfile(os.path.join(_path, year, 'eng.html')):
                    lang = 'eng'
            course_list[course]['editions'][year] = {
                    'year': int(year),
                    'org': org,
                    'lang': lang,
                    'title': title
                    }
    return course_list


# index
@app.route('/')
def view_index():
    items = publications.parse_bibtex(app.config['PUBLICATIONS_DB'])
    items = imap(publications.publication_formatter,
        items)
    selected_publications = ifilter(publications.is_selected, items)
    selected_publications = islice(selected_publications, 3)

    return page('index', data={
        'selected_publications': list(selected_publications)})


# talks
@app.route('/talks/')
def view_talks():
    return page('talks')


# research
@app.route('/research')
def view_research():
    return page('research')


# teaching
@app.route('/teaching/')
def view_teaching():
    return page(
            'teaching',
            data={'courses': courses()})


@app.route('/teaching/<course>/<year>/<lang>/')
def view_teaching_detail(course, year, lang='ita'):
    try:
        return page(
            'teaching',
            template='teaching/detail/%s/%s/%s.html' % (course, year, lang))
    except TemplateNotFound:
        return page404()



# publications
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

