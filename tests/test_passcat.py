import pytest
import subprocess
import sys
from passcat.passcat import generate, wordlists
import os

def test_wordlists_not_empty():
    wl = wordlists()
    assert isinstance(wl, list)
    assert len(wl) > 0
    for w in wl:
        assert isinstance(w, str)

def test_generate():
    # Use a small fixed wordlist for deterministic testing
    words = ['apple', 'banana', 'cherry']
    # Generate 3 words
    result = generate(words, 3)
    parts = result.split()
    assert len(parts) == 3
    for p in parts:
        assert p in words

def test_generate_single():
    words = ['apple']
    result = generate(words, 1)
    assert result == 'apple'

def test_generate_zero():
    words = ['apple', 'banana']
    result = generate(words, 0)
    assert result == ''

def test_generate_with_separator():
    words = ['apple', 'banana', 'cherry']
    # Test with custom separator
    result = generate(words, 3, separator='-')
    parts = result.split('-')
    assert len(parts) == 3
    for p in parts:
        assert p in words

def test_generate_with_empty_separator():
    words = ['apple', 'banana']
    result = generate(words, 2, separator='')
    # The result should be a concatenation of two words from the list (with replacement allowed)
    assert result in [w1 + w2 for w1 in words for w2 in words]

def test_positional_count():
    # Test that the positional argument for count works
    result = subprocess.run([sys.executable, '-m', 'passcat.passcat', '3'],
                            capture_output=True, text=True)
    assert result.returncode == 0
    words = result.stdout.strip().split()
    assert len(words) == 3

def test_count_option():
    # Test that the --count option works
    result = subprocess.run([sys.executable, '-m', 'passcat.passcat', '--count', '3'],
                            capture_output=True, text=True)
    assert result.returncode == 0
    words = result.stdout.strip().split()
    assert len(words) == 3

def test_count_option_overrides_positional():
    # According to our code, --count is checked first, then positional.
    # So if we pass both, --count should win.
    result = subprocess.run([sys.executable, '-m', 'passcat.passcat', '5', '--count', '3'],
                            capture_output=True, text=True)
    assert result.returncode == 0
    words = result.stdout.strip().split()
    assert len(words) == 3

def test_num_passphrases_default():
    # Test that by default only one passphrase is generated
    result = subprocess.run([sys.executable, '-m', 'passcat.passcat', '2'],
                            capture_output=True, text=True)
    assert result.returncode == 0
    lines = result.stdout.strip().split('\n')
    assert len(lines) == 1
    assert len(lines[0].split()) == 2

def test_num_passphrases_option():
    # Test that -n option generates multiple passphrases
    result = subprocess.run([sys.executable, '-m', 'passcat.passcat', '2', '-n', '3'],
                            capture_output=True, text=True)
    assert result.returncode == 0
    lines = result.stdout.strip().split('\n')
    assert len(lines) == 3
    for line in lines:
        assert len(line.split()) == 2

def test_num_passphrases_long_option():
    # Test that --num-passphrases option works
    result = subprocess.run([sys.executable, '-m', 'passcat.passcat', '1', '--num-passphrases', '2'],
                            capture_output=True, text=True)
    assert result.returncode == 0
    lines = result.stdout.strip().split('\n')
    assert len(lines) == 2
    for line in lines:
        assert len(line.split()) == 1

def test_num_passphrases_invalid():
    # Test that invalid input for -n gives error
    result = subprocess.run([sys.executable, '-m', 'passcat.passcat', '2', '-n', '0'],
                            capture_output=True, text=True)
    assert result.returncode != 0
    assert "Invalid num" in result.stderr or "Invalid num" in result.stdout

    result = subprocess.run([sys.executable, '-m', 'passcat.passcat', '2', '-n', '-1'],
                            capture_output=True, text=True)
    assert result.returncode != 0
    assert "Invalid num" in result.stderr or "Invalid num" in result.stdout

    result = subprocess.run([sys.executable, '-m', 'passcat.passcat', '2', '-n', 'abc'],
                            capture_output=True, text=True)
    assert result.returncode != 0
    assert "Invalid num" in result.stderr or "Invalid num" in result.stdout

if __name__ == '__main__':
    pytest.main([__file__])