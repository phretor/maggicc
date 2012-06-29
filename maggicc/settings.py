import os

class Config(object):
    DEBUG = False
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    STATIC_PATH = os.path.join(BASE_PATH, 'static')
    ASSETS_PATH = os.path.join(STATIC_PATH, 'assets')
    PUBLICATIONS_PATH = os.path.join(ASSETS_PATH, 'publications')

    #pages
    PAGES = {
        'index': {
            'visible': False,
            'title': 'Home'},
        'publications': {
            'visible': True,
            'gliph': 'j',
            'title': 'Publications'},
        'research': {
            'visible': True,
            'gliph': '`',
            'title': 'Research'},
        }

    #publications
    PUBLICATIONS_DB = os.path.join(BASE_PATH, 'data', 'publications.bib')
    PUBLICATIONS_TYPES_ORDER = (
                'Conference Papers',
                'Journal Papers',
                'Technical Reports',
                'Dissertations',
                'Miscellaneous')
    PUBLICATIONS_TYPES = {
            'inproceedings': 'Conference Papers',
            'article': 'Journal Papers',
            'techreport': 'Technical Reports',
            'report': 'Technical Reports',
            'phdthesis': 'Dissertations',
            'masterthesis': 'Dissertations',
            'default': 'Miscellaneous'}
