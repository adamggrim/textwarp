"""Tests for resolving ambiguous contractions based on context."""

from textwarp._core.providers.en.disambiguation import (
    disambiguate_ain_t,
    disambiguate_d,
    disambiguate_gotta,
    disambiguate_s,
    disambiguate_wanna,
    disambiguate_whatcha
)


def test_disambiguate_ain_t(get_contraction_span):
    """Test "ain't" disambiguation based on subject and verb tense."""
    assert disambiguate_ain_t(get_contraction_span(
        "I ain't no fortunate son.", "ain't"
    )) == 'am'
    assert disambiguate_ain_t(get_contraction_span(
        "He ain't heavy, he's my brother.", "ain't"
    )) == 'is'
    assert disambiguate_ain_t(get_contraction_span(
        "You ain't nothing but a hound dog.", "ain't"
    )) == 'are'
    assert disambiguate_ain_t(get_contraction_span(
        "Ain't got no life", "ain't"
    )) == 'has'
    assert disambiguate_ain_t(get_contraction_span(
        "You ain't seen nothing like me yet.", "ain't"
    )) == 'have'


def test_disambiguate_d(get_contraction_span):
    """Test "'d." disambiguation."""
    assert disambiguate_d(get_contraction_span(
        "I'd do anything for love.", "I'd"
    )) == 'would'
    assert disambiguate_d(get_contraction_span(
        "They'd seen his face before\n"
        'Nobody was really sure if he was from the House of Lords.', "They'd"
    )) == 'had'
    assert disambiguate_d(get_contraction_span(
        "Why'd you have to rain on my parade?", "Why'd"
    )) == 'did'
    assert disambiguate_d(get_contraction_span(
        "Guys, you know you'd better watch out.", "you'd"
    )) == 'had'


def test_disambiguate_gotta(get_contraction_span):
    """Test "gotta" disambiguation."""
    assert disambiguate_gotta(get_contraction_span(
        "'Cause I gotta have faith.", 'gotta'
    )) == 'to'
    assert disambiguate_gotta(get_contraction_span(
        "I gotta feelin.'.", 'gotta'
    )) == 'a'


def test_disambiguate_s(get_contraction_span):
    """Test "'s" disambiguation."""
    assert disambiguate_s(get_contraction_span(
        "She's a woman who understands.", "She's"
    )) == 'is'
    assert disambiguate_s(get_contraction_span(
        "It's been 14 years.", "It's")) == "has"
    assert disambiguate_s(get_contraction_span(
        "Let's go girls.", "Let's"
    )) == 'us'
    assert disambiguate_s(get_contraction_span(
        "How's it feel to be on your own?", "How's"
    )) == 'does'


def test_disambiguate_wanna(get_contraction_span):
    """Test "wanna" disambiguation."""
    assert disambiguate_wanna(get_contraction_span(
        'I wanna hold your hand.', 'wanna'
    )) == 'to'
    assert disambiguate_wanna(get_contraction_span(
        'You wanna piece of me?', 'wanna'
    )) == 'a'


def test_disambiguate_whatcha(get_contraction_span):
    """Test "whatcha" disambiguation."""
    assert disambiguate_whatcha(get_contraction_span(
        "Chill out, whatcha yellin' for?", 'whatcha'
    )) == 'are'
    assert disambiguate_whatcha(get_contraction_span(
        "Show 'em whatcha got.", 'whatcha'
    )) == 'have'
    assert disambiguate_whatcha(get_contraction_span(
        'Tell me whatcha want, whatcha really, really want.', 'whatcha'
    )) == 'do'
