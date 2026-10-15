from textwarp._core.providers.en.casing import (
    case_from_string,
    is_lowercase_particle_or_affix,
    should_capitalize_in_title
)
from textwarp._lib.nlp import process_as_doc


def test_case_from_string_pronoun_i():
    assert case_from_string('i') == 'I'
    assert case_from_string('i', lowercase_by_default=True) == 'I'


def test_case_from_string_abbreviations():
    assert case_from_string('e.g.', lowercase_by_default=True) == 'e.g.'
    assert case_from_string('e.g.,', lowercase_by_default=True) == 'e.g.,'
    assert case_from_string('vs.', lowercase_by_default=True) == 'vs.'


def test_case_from_string_initialisms():
    assert case_from_string('u.s.a.') == 'U.S.A.'
    assert case_from_string('ph.d.') == 'Ph.D.'
    assert case_from_string("u.s.a.'s") == "U.S.A.'s"
    assert case_from_string('ph.d.’s') == 'Ph.D.’s'


def test_case_from_string_absolute_map():
    assert case_from_string('nato') == 'NATO'
    assert case_from_string('macos') == 'macOS'
    assert case_from_string('iphone') == 'iPhone'


def test_case_from_string_map_suffix():
    """Test that dictionary capitalization preserves contraction
    suffixes.
    """
    assert case_from_string("nato's") == "NATO's"
    assert case_from_string("ceo's") == "CEO's"


def test_case_from_string_prefixed_surname():
    assert case_from_string('macarthur') == 'MacArthur'
    assert case_from_string('mackay') == 'MacKay'
    assert case_from_string('mcgregor') == 'McGregor'
    assert case_from_string('o’connor') == 'O’Connor'


def test_case_from_string_prefixed_surname_exception():
    assert case_from_string('macaw') == 'Macaw'
    assert case_from_string('macbeth') == 'Macbeth'
    assert case_from_string('machiavelli') == 'Machiavelli'
    assert case_from_string('machine') == 'Machine'
    assert case_from_string('mace') == 'Mace'
    assert case_from_string('mach') == 'Mach'
    assert case_from_string('o’er') == 'O’er'


def test_case_from_string_mixed_case():
    mixed_word = 'shakenNotStirred'
    assert case_from_string(mixed_word) == mixed_word
    assert (
        case_from_string(mixed_word, preserve_mixed_case=False)
        == 'Shakennotstirred'
    )


def test_case_from_string_fallback():
    assert case_from_string('muffin') == 'Muffin'
    assert case_from_string('muffin', lowercase_by_default=True) == 'muffin'


def test_is_lowercase_particle_or_affix():
    assert is_lowercase_particle_or_affix('von') is True
    assert is_lowercase_particle_or_affix("n't") is True
    assert is_lowercase_particle_or_affix('n’t') is True
    assert is_lowercase_particle_or_affix('The') is False


def test_should_capitalize_in_title_lowercase_particles():
    doc = process_as_doc('Maria Augusta von Trapp')
    von_token = doc[2]

    assert von_token.lower_ == 'von'
    assert should_capitalize_in_title(von_token) is False


def test_should_capitalize_in_title_contraction_suffixes():
    doc = process_as_doc('don’t, don’t')
    nt_token = doc[4]

    assert nt_token.lower_ == 'n’t'
    assert should_capitalize_in_title(nt_token) is False


def test_should_capitalize_in_title_length():
    doc = process_as_doc('about')
    token = doc[0]

    assert len(token.text) >= 5
    assert should_capitalize_in_title(token) is True


def test_should_capitalize_in_title_pos_exception():
    doc = process_as_doc('and')
    token = doc[0]

    assert token.pos_ in {'CCONJ', 'CONJ'} or token.tag_ == 'CC'
    assert should_capitalize_in_title(token) is False


def test_should_capitalize_in_title_normal():
    doc = process_as_doc('wheelbarrow')
    token = doc[0]

    assert should_capitalize_in_title(token) is True
