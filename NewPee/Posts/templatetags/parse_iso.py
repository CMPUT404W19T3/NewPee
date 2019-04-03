# https://stackoverflow.com/questions/34012527/how-to-parse-2015-01-01t000000z-in-django-template
# https://stackoverflow.com/questions/969285/how-do-i-translate-an-iso-8601-datetime-string-into-a-python-datetime-object
from django.template import Library

import dateutil.parser

register = Library()

@register.filter(expects_localtime=True)
def parse_iso(value):
    return dateutil.parser.parse(value)
    #return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")