import pytest
import subprocess
import sys
from passcat.passcat import generate, generate_unique, wordlists
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

def test_generate_with_transform():
    words = ['apple', 'banana', 'cherry']
    # Test capitalize transform
    result = generate(words, 3, transform=str.capitalize)
    parts = result.split()
    assert len(parts) == 3
    for part in parts:
        assert part == part.capitalize()
    # Test uppercase transform
    result = generate(words, 3, transform=str.upper)
    parts = result.split()
    assert len(parts) == 3
    for part in parts:
        assert part == part.upper()

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

def test_capitalize_option():
    # Test that -C option runs without error and produces two words
    result = subprocess.run([sys.executable, '-m', 'passcat.passcat', '2', '-C'],
                            capture_output=True, text=True)
    assert result.returncode == 0
    line = result.stdout.strip()
    words = line.split()
    assert len(words) == 2
    # Each word should be non-empty
    for word in words:
        assert len(word) > 0

def test_uppercase_option():
    # Test that -U option converts all letters to uppercase
    result = subprocess.run([sys.executable, '-m', 'passcat.passcat', '2', '-U'],
                            capture_output=True, text=True)
    assert result.returncode == 0
    line = result.stdout.strip()
    words = line.split()
    assert len(words) == 2
    for word in words:
        assert word == word.upper()

def test_capitalize_with_separator():
    # Test that -C works with custom separator
    result = subprocess.run([sys.executable, '-m', 'passcat.passcat', '2', '-C', '--separator', '-'],
                            capture_output=True, text=True)
    assert result.returncode == 0
    line = result.stdout.strip()
    assert '-' in line
    parts = line.split('-')
    assert len(parts) == 2
    for part in parts:
        assert len(part) > 0

def test_uppercase_with_count():
    # Test that -U works with --count option
    result = subprocess.run([sys.executable, '-m', 'passcat.passcat', '--count', '2', '-U'],
                            capture_output=True, text=True)
    assert result.returncode == 0
    line = result.stdout.strip()
    words = line.split()
    assert len(words) == 2
    for word in words:
        assert word == word.upper()

def test_no_separator():
    # Test that --no-separator produces output without spaces
    result = subprocess.run([sys.executable, '-m', 'passcat.passcat', '2', '--no-separator'],
                            capture_output=True, text=True)
    assert result.returncode == 0
    line = result.stdout.strip()
    # Should be two words concatenated without space
    assert len(line) > 0
    assert ' ' not in line

def test_unique():
    # Test that --unique prevents repeated words in a passphrase
    # Use a small wordlist for testing by creating a temporary one? 
    # Instead, we can test with the default wordlist and just check that the two words are different.
    # Note: There is a small chance they are the same, but with a large wordlist it's negligible.
    # For deterministic testing, we would need to mock choice, but for simplicity we'll just run and check.
    result = subprocess.run([sys.executable, '-m', 'passcat.passcat', '2', '--unique'],
                            capture_output=True, text=True)
    assert result.returncode == 0
    line = result.stdout.strip()
    words = line.split()
    assert len(words) == 2
    # The two words should be different
    assert words[0] != words[1]

def test_unique_with_separator():
    # Test that --unique works with custom separator
    result = subprocess.run([sys.executable, '-m', 'passcat.passcat', '2', '--unique', '--separator', '-'],
                            capture_output=True, text=True)
    assert result.returncode == 0
    line = result.stdout.strip()
    assert '-' in line
    parts = line.split('-')
    assert len(parts) == 2
    assert parts[0] != parts[1]

def test_unique_uppercase():
    # Test that --unique works with --uppercase
    result = subprocess.run([sys.executable, '-m', 'passcat.passcat', '2', '--unique', '-U'],
                            capture_output=True, text=True)
    assert result.returncode == 0
    line = result.stdout.strip()
    words = line.split()
    assert len(words) == 2
    assert words[0] != words[1]
    for word in words:
        assert word == word.upper()

if __name__ == '__main__':
    pytest.main([__file__])