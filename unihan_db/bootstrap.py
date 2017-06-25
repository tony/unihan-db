# -*- coding: utf8 - *-
from __future__ import (absolute_import, print_function, unicode_literals,
                        with_statement)

import logging
from datetime import datetime

from sqlalchemy import create_engine, event
from sqlalchemy.orm import class_mapper, mapper, scoped_session, sessionmaker
from unihan_etl import process as unihan

from . import dirs, importer
from .tables import Base, Unhn
from .util import merge_dict


log = logging.getLogger(__name__)


def setup_logger(logger=None, level='INFO'):
    """Setup logging for CLI use.

    :param logger: instance of logger
    :type logger: :py:class:`Logger`

    """
    if not logger:
        logger = logging.getLogger()
    if not logger.handlers:
        channel = logging.StreamHandler()

        logger.setLevel(level)
        logger.addHandler(channel)


setup_logger()


UNIHAN_FILES = [
    'Unihan_DictionaryIndices.txt',
    'Unihan_DictionaryLikeData.txt',
    'Unihan_IRGSources.txt',
    'Unihan_NumericValues.txt',
    'Unihan_RadicalStrokeCounts.txt',
    'Unihan_Readings.txt', 'Unihan_Variants.txt'
]

UNIHAN_FIELDS = [
    'kAccountingNumeric', 'kCangjie', 'kCantonese', 'kCheungBauer',
    'kCihaiT', 'kCompatibilityVariant', 'kDefinition', 'kFenn',
    'kFourCornerCode', 'kFrequency', 'kGradeLevel', 'kHDZRadBreak',
    'kHKGlyph', 'kHangul', 'kHanyuPinlu', 'kHanYu', 'kHanyuPinyin',
    'kJapaneseKun', 'kJapaneseOn', 'kKorean', 'kMandarin',
    'kOtherNumeric', 'kPhonetic', 'kPrimaryNumeric',
    'kRSAdobe_Japan1_6', 'kRSJapanese', 'kRSKanWa', 'kRSKangXi',
    'kRSKorean', 'kRSUnicode', 'kSemanticVariant',
    'kSimplifiedVariant', 'kSpecializedSemanticVariant', 'kTang',
    'kTotalStrokes', 'kTraditionalVariant', 'kVietnamese', 'kXHC1983',
    'kZVariant'
]

UNIHAN_ETL_DEFAULT_OPTIONS = {
    'input_files': UNIHAN_FILES,
    'fields': UNIHAN_FIELDS,
    'format': 'python',
    'expand': True
}


TABLE_NAME = 'Unihan'


DEFAULT_FIELDS = ['ucn', 'char']


def is_bootstrapped(metadata):
    """Return True if cihai is correctly bootstrapped."""
    fields = UNIHAN_FIELDS + DEFAULT_FIELDS
    if TABLE_NAME in metadata.tables.keys():
        table = metadata.tables[TABLE_NAME]

        if set(fields) == set(c.name for c in table.columns):
            return True
        else:
            return False
    else:
        return False


def bootstrap_data(options={}):
    options = merge_dict(UNIHAN_ETL_DEFAULT_OPTIONS.copy(), options)

    p = unihan.Packager(options)
    p.download()
    return p.export()


def bootstrap_unihan(session, options={}):
    """Download, extract and import unihan to database."""
    if session.query(Unhn).count() == 0:
        data = bootstrap_data(options)
        log.info('bootstrap Unhn table')
        log.info('bootstrap Unhn table finished')
        count = 0
        items = []
        for char in data:
            c = Unhn(char=char['char'], ucn=char['ucn'])
            importer.import_char(c, char)
            items.append(c)

            count += 1
            log.debug("imported %s: complete %s" % (char['char'], count))
        session.add_all(items)
        session.commit()


def to_dict(obj, found=None):
    """Return dictionary of an SQLAlchemy Query result.

    Supports recursive relationships.

    :param obj: SQLAlchemy Query result
    :type obj: :class:`sqlalchemy.orm.query.Query` result object
    :param found: recursive parameter
    :type found: :class:`python:set`
    :returns: dictionary of results
    :rtype: :class:`python:dict`
    """

    def _get_key_value(c):
        if isinstance(getattr(obj, c), datetime):
            return (c, getattr(obj, c).isoformat())
        else:
            return (c, getattr(obj, c))

    if found is None:
        found = set()
    mapper = class_mapper(obj.__class__)
    columns = [column.key for column in mapper.columns]

    result = dict(map(_get_key_value, columns))
    for name, relation in mapper.relationships.items():
        if relation not in found:
            found.add(relation)
            related_obj = getattr(obj, name)
            if related_obj is not None:
                if relation.uselist:
                    result[name] = [
                        to_dict(child, found) for child in related_obj
                    ]
                else:
                    result[name] = to_dict(related_obj, found)
    return result


def add_to_dict(b):
    """Add :func:`.to_dict` method to SQLAlchemy Base object.

    :param b: SQLAlchemy Base class
    :type b: :func:`~sqlalchemy:sqlalchemy.ext.declarative.declarative_base`
    """
    b.to_dict = to_dict
    return b


def get_session(engine_url='sqlite:///{user_data_dir}/unihan_db.db'):
    """Return new SQLAlchemy session object from engine string.

    *engine_url* accepts a string template variable for ``{user_data_dir}``,
    which is replaced to the XDG data directory for the user running the script
    process. This variable is only useful for SQLite, where file paths are
    used for the engine_url.

    :param engine_url: SQLAlchemy engine string
    :type engine_url: string
    """

    engine_url = engine_url.format(**{
        'user_data_dir': dirs.user_data_dir,
    })
    engine = create_engine(engine_url)

    event.listen(mapper, 'after_configured', add_to_dict(Base))
    Base.metadata.bind = engine
    Base.metadata.create_all()
    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)

    return session
