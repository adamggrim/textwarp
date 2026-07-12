"""Tests for command-line input and output functions."""

import os
import shutil
import pytest

from textwarp._cli.ui import (
    get_input,
    print_padding,
    print_wrapped,
    program_exit,
    prompt_for_integer
)
from textwarp._cli.constants.messages import (
    ANY_OTHER_TEXT_PROMPT,
    ENTER_VALID_RESPONSE_PROMPT,
    EXIT_MSG
)


def test_get_input_delay(simulate_input, monkeypatch):
    sleep_called = False

    def mock_sleep(seconds):
        nonlocal sleep_called
        sleep_called = True
        assert seconds == 0.5

    monkeypatch.setattr('time.sleep', mock_sleep)
    simulate_input(['y'])

    get_input()
    assert sleep_called is True


def test_get_input_no_or_exit(simulate_input):
    simulate_input(['n'])
    assert get_input() is False

    simulate_input(['quit'])
    assert get_input() is False


def test_get_input_yes(simulate_input):
    simulate_input(['y'])
    assert get_input() is True

    simulate_input(['yes'])
    assert get_input() is True


def test_get_input_invalid_then_valid(simulate_input, capsys):
    simulate_input(['invalid', 'wrong', 'y'])

    assert get_input() is True

    captured = capsys.readouterr()
    assert ANY_OTHER_TEXT_PROMPT in captured.out
    assert ENTER_VALID_RESPONSE_PROMPT in captured.out


def test_print_padding(capsys):
    print_padding()
    captured = capsys.readouterr()
    assert captured.out == '\n'


def test_print_wrapped(monkeypatch, capsys):
    monkeypatch.setattr(
        shutil,
        'get_terminal_size',
        lambda fallback=None: os.terminal_size((20, 24))
    )

    long_text = (
        'It was the best of times, it was the worst of times, it was the age '
        'of wisdom, it was the age of foolishness, it was the epoch of '
        'belief, it was the epoch of incredulity, it was the season of Light, '
        'it was the season of Darkness, it was the spring of hope, it was the '
        'winter of despair, we had everything before us, we had nothing '
        'before us, we were all going direct to Heaven, we were all going '
        'direct the other way—in short, the period was so far like the '
        'present period, that some of its noisiest authorities insisted on '
        'its being received, for good or for evil, in the superlative degree '
        'of comparison only.'
    )
    print_wrapped(long_text)

    captured = capsys.readouterr()
    assert captured.out.startswith('\n')

    lines = captured.out.strip().split('\n')
    for line in lines:
        assert len(line) <= 19


def test_program_exit(capsys):
    with pytest.raises(SystemExit):
        program_exit()

    captured = capsys.readouterr()
    assert EXIT_MSG in captured.out


def test_prompt_for_integer_exit(simulate_input, capsys):
    simulate_input(['q'])

    with pytest.raises(SystemExit):
        prompt_for_integer('Enter number:', 'Invalid', allow_early_exit=True)

    captured = capsys.readouterr()
    assert EXIT_MSG in captured.out


def test_prompt_for_integer_valid(simulate_input):
    simulate_input(['42'])
    assert prompt_for_integer('Enter number:', 'Invalid') == 42


def test_prompt_for_integer_invalid_then_valid(simulate_input, capsys):
    simulate_input(['abc', '-5', '0', '7'])

    assert prompt_for_integer('Enter number:', 'Invalid number!') == 7

    captured = capsys.readouterr()
    assert 'Enter number:' in captured.out
    assert 'Invalid number!' in captured.out
    assert captured.out.count('Invalid number!') == 3
