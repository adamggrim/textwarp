import pytest

from textwarp._core.providers.en.expansion.disambiguation import (
    disambiguate_ain_t,
    disambiguate_d,
    disambiguate_gotta_or_wanna,
    disambiguate_s,
    disambiguate_whatcha
)


@pytest.mark.parametrize('text, contraction, expected', [
    ('I ain’t no fortunate son.', 'ain’t', 'am'),
    ('He ain’t heavy, he’s my brother.', 'ain’t', 'is'),
    ('You ain’t bad. You ain’t nothing!', 'ain’t', 'are'),
    ('Ain’t got no life', 'ain’t', 'has'),
    ('You ain’t seen nothing like me yet.', 'ain’t', 'have'),
    ('I ain’t never crossed a man that didn’t deserve it.', 'ain’t', 'have')
])
def test_disambiguate_ain_t(get_contraction_span, text, contraction, expected):
    assert disambiguate_ain_t(
        get_contraction_span(text, contraction)
    ) == expected

@pytest.mark.parametrize('text, contraction, expected', [
    ('I’d do anything for love.', 'I’d', 'would'),
    (
        'They’d seen his face before\n'
        'Nobody was really sure if he was from the House of Lords.',
        'They’d', 'had'
    ),
    ('Why’d you have to rain on my parade?', 'Why’d', 'did'),
    ('I’d just stare out my window.', 'I’d', 'would'),
    ('Guys, you know you’d better watch out.', 'you’d', 'had')
])
def test_disambiguate_d(get_contraction_span, text, contraction, expected):
    assert disambiguate_d(get_contraction_span(text, contraction)) == expected

@pytest.mark.parametrize('text, contraction, expected', [
    ('’Cause I gotta have faith.', 'gotta', 'to'),
    ('I gotta feelin’.', 'gotta', 'a'),
    ('I wanna hold your hand.', 'wanna', 'to'),
    ('You wanna piece of me?', 'wanna', 'a')
])
def test_disambiguate_gotta_or_wanna(
    get_contraction_span, text,
    contraction, expected
):
    assert disambiguate_gotta_or_wanna(
        get_contraction_span(text, contraction)
    ) == expected

@pytest.mark.parametrize('text, contraction, expected', [
    ('She’s a woman who understands.', 'She’s', 'is'),
    ('It’s been 14 years.', 'It’s', 'has'),
    ('Let’s go girls.', 'Let’s', 'us'),
    ('How’s it feel to be on your own?', 'How’s', 'does'),
    ('Bennie, she’s really keen', 'She’s', 'is'),
    (
        'It’s always times like these when I think of you\n'
        'And I wonder if you ever think of me', 'It’s', 'is'
    )
])
def test_disambiguate_s(get_contraction_span, text, contraction, expected):
    assert disambiguate_s(get_contraction_span(text, contraction)) == expected

@pytest.mark.parametrize('text, contraction, expected', [
    ('Chill out, whatcha yellin’ for?', 'whatcha', 'are'),
    ('Show ’em whatcha got.', 'whatcha', 'have'),
    ('Tell me whatcha want, whatcha really, really want.', 'whatcha', 'do')
])
def test_disambiguate_whatcha(
    get_contraction_span, text,
    contraction, expected
):
    assert disambiguate_whatcha(
        get_contraction_span(text, contraction)
    ) == expected
