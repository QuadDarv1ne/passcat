# Notes on passcat project

## Overview
Passcat is a tool for generating cryptographically secure, memorable passphrases.

## Features
- Generates passphrases from built-in wordlists (EFF, English, etc.)
- Supports custom wordlists via file path
- Options for number of words, number of passphrases, separator, capitalization, uppercase, no separator, unique words
- Shows wordlist information with --show-wordlist

## Recent Changes
- Added --show-wordlist option to display information about the selected wordlist.
- Added comprehensive tests for the new feature.

## Potential Improvements
- Consider adding more wordlists.
- Allow combining multiple wordlists.
- Add option to exclude certain characters or words.