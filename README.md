# Passcat

Passcat lets you generate cryptographically secure, memorable passphrases.

## Installation

``pip install passcat``

## Usage

Basic usage:

```
$ passcat
throng disregard overall trimming playpen persevere
```

Specify the number of words to use in the passphrase:

```
$ passcat 5
relight usage geologic tumbling disown
```

or

```
$ passcat --count 5
relight usage geologic tumbling disown
```

Show available wordlists:

```
$ passcat -l

Eff
English
French
German
Indonesian
Italian
Spanish
```

Specify a wordlist other than EFF:

```
$ passcat -w spanish
latitar reglamentaria apanuscadora consultable carbunclo duplicar paragueria cincoanal
```

Specify the path to an alternate wordlist:

``$ passcat -f /path/to/wordlist/file.txt``

Specify the separator between words (default is space):

```
$ passcat 3 --separator '-'
correct-horse-battery
```

Generate multiple passphrases at once:

```
$ passcat 2 -n 3
word1 word2
word3 word4
word5 word6
```

Capitalize the first letter of each word:

```
$ passcat 2 -C
Apple Banana
Cherry Date
```

Convert all letters to uppercase:

```
$ passcat 2 -U
APPLE BANANA
CHERRY DATE
```

Do not use a separator between words:

```
$ passcat 2 --no-separator
word1word2
```

Ensure no repeated words in the passphrase:

```
$ passcat 3 --unique
word1 word2 word3
```

Combine options:

```
$ passcat 2 -n 2 -C --separator '.' --unique
Apple.Banana
Cherry.Date
```

## License

This code is released under a free software [license](LICENSE.txt) and you are welcome to fork it.