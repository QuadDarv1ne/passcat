#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Passcat lets you generate cryptographically secure, memorable passphrases.

Usage:
    passcat [COUNT] [--file=f] [--help] [--list] [--version] [--wordlist=w]
            [--separator=s] [--count=c] [-n NUM]

Options:
    -f --file=f               Specify the path to an alternate wordlist.
    -h --help                 Show this message.
    -l --list                 Show available wordlists.
    -v --version              Show version.
    -w --wordlist=w           Specify a wordlist. [default: eff]
    -s --separator=s  Specify the separator between words. [default: ' ']
    -c --count=c          Specify the number of words.
    -n --num-passphrases=NUM  Specify the number of passphrases to generate.
"""

import os
import sys
import docopt

from . import __version__
from secrets import choice

_dir = os.path.dirname(os.path.abspath(__file__))


def wordlists():
    """
    List available wordlists.
    """
    return [a.replace('.txt', '').capitalize()
            for a in os.listdir(_dir+'/wordlists/')
            if a.endswith('.txt')]


def generate(words, count, separator=' '):
    """
    Generate passphrase.
    """
    return separator.join(choice(words) for i in range(count))


def main():
    args = docopt.docopt(__doc__, version=__version__)

    if args['--list']:
        print('\n'.join(sorted(wordlists())))
        sys.exit(0)

    path = args['--file']
    if path is None:
        path = '%s/wordlists/%s.txt' % (_dir, args['--wordlist'].lower())

    try:
        with open(path) as f:
            words = f.read().splitlines()
    except FileNotFoundError:
        print("File not found. Please input the path of an existing "
              "file or use the '-l' flag to show available wordlists.")
        sys.exit(1)

    # Determine count: prefer --count, then positional, then default 6
    count_arg = args['--count']
    if count_arg is None:
        count_arg = args['COUNT']
    if count_arg is None:
        count = 6
    else:
        if not str(count_arg).isdigit():
            print("Invalid count. Enter a valid number.")
            sys.exit(1)
        count = int(count_arg)

    # Determine number of passphrases to generate
    num_passphrases_arg = args['--num-passphrases']
    if num_passphrases_arg is None:
        num_passphrases = 1
    else:
        if (not str(num_passphrases_arg).isdigit() or
                int(num_passphrases_arg) < 1):
            print("Invalid num. Enter a positive integer.")
            sys.exit(1)
        num_passphrases = int(num_passphrases_arg)

    separator = args['--separator']
    if separator is None:
        separator = ' '

    for _ in range(num_passphrases):
        passphrase = generate(words, count, separator)
        print(passphrase)


if __name__ == '__main__':
    main()
