"""Tests for text cleaning functions."""

from hypothesis import given, strategies

from textwarp._lib.cleaning import (
    strip_html,
    to_single_spaces
)


def test_strip_html():
    assert strip_html(
        '<p>I do HTML for ’em <b>all</b>!</p>'
    ) == 'I do HTML for ’em all!'
    assert strip_html('I edit Wikipedia.') == 'I edit Wikipedia.'
    assert strip_html(
        'AV club &lt; glee club &gt; chess team'
    ) == 'AV club < glee club > chess team'


def test_to_single_spaces():
    assert to_single_spaces(
        'Objects  In  The  Rear  View  Mirror  May  Appear  Closer  Than  '
        'They  Are'
    ) == 'Objects In The Rear View Mirror May Appear Closer Than They Are'
    assert (
        to_single_spaces('\tCome   together,   right   now')
        == '\tCome together, right now'
    )

@given(strategies.text())
def test_strip_html_no_crash(s):
    result = strip_html(s)
    assert isinstance(result, str)
