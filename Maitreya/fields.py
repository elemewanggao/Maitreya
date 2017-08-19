# -*- coding=utf-8 -*-

from webargs.fields import *
from marshmallow import utils, validate
from marshmallow.fields import ValidatedField, Integer
import datetime as dt

from Maitreya.utils.common import MAX_I32, MAX_I64


class DateStr(Field):
    """ISO8601-formatted date string.

    :param kwargs: The same keyword arguments that :class:`Field` receives.
    """
    default_error_messages = {
        'invalid': 'Not a valid date.',
        'format': '"{input}" cannot be formatted as a date.',
    }

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        try:
            return value.isoformat()
        except AttributeError:
            self.fail('format', input=value)
        return value

    def _deserialize(self, value, attr, data):
        """Deserialize an ISO8601-formatted date string to a
        :class:`datetime.date` object.
        """
        if not value:  # falsy values are invalid
            self.fail('invalid')
        try:
            return utils.from_iso_date(value).strftime("%Y-%m-%d")
        except (AttributeError, TypeError, ValueError):
            self.fail('invalid')


class DateTimeStr(Field):
    """A formatted datetime string in UTC.

    Example: ``'2014-12-22T03:12:58.019077+00:00'``

    Timezone-naive `datetime` objects are converted to
    UTC (+00:00) by :meth:`Schema.dump <marshmallow.Schema.dump>`.
    :meth:`Schema.load <marshmallow.Schema.load>` returns `datetime`
    objects that are timezone-aware.

    :param str format: Either ``"rfc"`` (for RFC822), ``"iso"`` (for ISO8601),
        or a date format string. If `None`, defaults to "iso".
    :param kwargs: The same keyword arguments that :class:`Field` receives.

    """

    DATEFORMAT_SERIALIZATION_FUNCS = {
        'iso': utils.isoformat,
        'iso8601': utils.isoformat,
        'rfc': utils.rfcformat,
        'rfc822': utils.rfcformat,
    }

    DATEFORMAT_DESERIALIZATION_FUNCS = {
        'iso': utils.from_iso,
        'iso8601': utils.from_iso,
        'rfc': utils.from_rfc,
        'rfc822': utils.from_rfc,
    }

    DEFAULT_FORMAT = 'iso'

    localtime = False
    default_error_messages = {
        'invalid': 'Not a valid datetime.',
        'format': '"{input}" cannot be formatted as a datetime.',
    }

    def __init__(self, format=None, **kwargs):
        super(DateTimeStr, self).__init__(**kwargs)
        # Allow this to be None. It may be set later in the ``_serialize``
        # or ``_desrialize`` methods This allows a Schema to dynamically set the
        # dateformat, e.g. from a Meta option
        self.dateformat = format or "%Y-%m-%d %H:%M:%S"

    def _add_to_schema(self, field_name, schema):
        super(DateTime, self)._add_to_schema(field_name, schema)
        self.dateformat = self.dateformat or schema.opts.dateformat

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        self.dateformat = self.dateformat or self.DEFAULT_FORMAT
        format_func = self.DATEFORMAT_SERIALIZATION_FUNCS.get(
            self.dateformat, None)
        if format_func:
            try:
                return format_func(value, localtime=self.localtime)
            except (AttributeError, ValueError):
                self.fail('format', input=value)
        else:
            return value.strftime(self.dateformat)

    def _deserialize(self, value, attr, data):
        if not value:  # Falsy values, e.g. '', None, [] are not valid
            raise self.fail('invalid')
        if self.dateformat:
            try:
                return dt.datetime.strptime(value, self.dateformat)\
                        .strftime('%Y-%m-%d %H:%M:%S')
            except (TypeError, AttributeError, ValueError):
                raise self.fail('invalid')
        else:
            warnings.warn('It is recommended that you install python-dateutil '
                          'for improved datetime deserialization.')
            raise self.fail('invalid')


class IntergerRange(ValidatedField, Integer):
    """Base class for Integer between min and max"""
    default_error_messages = {
        "invalid": "Not a valid unsigned 32 bit integer."
    }

    def __init__(self, *args, **kwargs):
        Integer.__init__(self, *args, **kwargs)
        # Insert validation into self.validators so that
        # multiple errors can be stored.
        self.validators.insert(0, validate.Range(
            error=self.error_messages['invalid'])
        )

    def _validated(self, value):
        if value is None:
            return None
        return validate.Range(
            min=self.range_min,
            max=self.range_max,
            error=self.error_messages['invalid']
        )(Integer._validated(self, value))


class Interger32(IntergerRange):
    range_min = 0
    range_max = MAX_I32


class Interger64(IntergerRange):
    range_min = 0
    range_max = MAX_I64


Int32 = Interger32
Int64 = Interger64
