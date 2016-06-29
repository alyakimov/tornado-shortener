from __future__ import absolute_import, division, print_function, with_statement

from wtforms import SubmitField, validators
from wtforms_html5 import URLField
from wtforms_tornado import Form


class ShotenerForm(Form):
    uri = URLField("Paste your long URL here:", [validators.DataRequired()])
    submit = SubmitField('Shorten URL')
