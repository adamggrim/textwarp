# Textwarp

`textwarp` is a Python package for analyzing and transforming text. For the given text, `textwarp` applies a transformation or analysis function and copies any modified text to the clipboard.

## Requirements

- Python 3.10+

## Dependencies

`textwarp` requires the following Python libraries:

- `pyperclip`: For accessing and copying to the clipboard
- `regex`: For regular expressions with variable-width lookbehinds
- `spacy[transformers]`: For identifying word context using transformer-based models

## Example

This example demonstrates how to convert text to camel case using `textwarp`.

1. **Copy text to the clipboard**

    In this example, `textwarp` will modify the following clipboard text: `The mind is its own place`.

2. **Run the command**

    Once the text is copied to the clipboard, call `textwarp` from the command line. Enter a required argument for the desired clipboard modification: `textwarp --camel-case`

    For a comprehensive list of `textwarp` arguments, type `textwarp -h` or `textwarp --help`:
    ```
    -h, --help             show this help message and exit
    --version              show version number and exit
    --alternating-caps     cOnVeRt To AlTeRnAtInG cApS
    --binary               convert to binary
    --camel-case           convertToCamelCase
    --capitalize           Capitalize The First Character Of Each Word
    --cardinal             convert ordinal numbers to cardinal numbers
    --char-count           count characters
    --clear                clear clipboard text
    --curly-quotes         convert "straight quotes" to “curly quotes”
    --dot-case             convert.to.dot.case
    --expand-contractions  expand contractions
    --from-binary          convert from binary
    --from-hexadecimal     convert from hexadecimal
    --from-morse           convert from Morse code
    --hexadecimal          convert to hexadecimal
    --hyphens-to-em        convert consecutive hyphens to em dashes
    --hyphen-to-en         convert hyphens to en dashes
    --kebab-case           convert-to-kebab-case
    --line-count           count lines
    --lowercase            convert to lowercase
    --mfws                 get most frequent words
    --morse                convert to Morse code
    --ordinal              convert cardinal numbers to ordinal numbers
    --pascal-case          ConvertToPascalCase
    --plain-text           convert to plain text
    --pos-count            count parts of speech
    --punct-to-inside      "move punctuation inside quotation marks."
    --punct-to-outside     "move punctuation outside quotation marks".
    --random-case          randomize the casing of each character
    --randomize            randomize characters
    --redact               redact text
    --replace              find and replace text
    --replace-case         find and replace a case
    --replace-regex        find and replace a regular expression
    --reverse              reverse text
    --sentence-case        Convert to sentence case.
    --sentence-count       count sentences
    --single-spaces        convert consecutive spaces to a single space
    --snake-case           convert_to_snake_case
    --straight-quotes      convert “curly quotes” to "straight quotes"
    --strip                remove leading and trailing whitespace
    --swapcase             convert LOWERCASE to all caps and vice versa
    --time-to-read         calculate time to read
    --title-case           Convert to Title Case
    --uppercase            CONVERT TO ALL CAPS
    --word-count           count words
    --widen                w i d e n  t e x t
    ```

3. **Paste text from the clipboard**

    `textwarp` will copy the modified text to the clipboard: `theMindIsItsOwnPlace`. To view the modified text, paste from the clipboard.

4. **Continue or exit**

    The program will prompt you to copy any other text to the clipboard. To exit, type `no` (`n`), `quit` (`q`) or `exit` (`e`), or trigger a KeyboardInterrupt (Ctrl + C):

    ```
    Any other text? (y/n) (Copy text to clipboard):
    ^C

    Exiting the program...
    ```

## Structure

```
textwarp/
├── _cli/
│ ├── constants/
│ │ ├── __init__.py: Exposes command-line inputs and messages
│ │ ├── inputs.py: Sets for command-line input
│ │ └── messages.py: Strings for displaying command-line messages
│ ├── __init__.py: Initializes the _cli sub-package
│ ├── args.py: A mapping of command-line arguments to functions and help messages
│ ├── dispatch.py: A mapping of string inputs to case conversion functions
│ ├── formatting.py: Functions for formatting analysis into readable strings
│ ├── parsing.py: Command-line argument parsing using argparse
│ ├── runners.py: Main loop logic for executing commands
│ ├── ui.py: Functions for handling console input and output
│ └── validation.py: Validators for text, clipboard, and regular expression content
├── _commands/
│ ├── __init__.py: Exposes analysis and replacement commands for use across the package
│ ├── analysis.py: Runners for analysis commands
│ └── replacement.py: Runners for replacement commands
├── _core/
│ ├── constants/
│ │ ├── __init__.py: Exposes constants for use across the package
│ │ ├── apostrophes.py: Set used across the package for grouping apostrophe characters
│ │ ├── maps.py: Map used across the package for lookups
│ │ ├── nlp.py: Objects used across the package for spaCy processing
│ │ └── regexes.py: Regular expressions used across the package
│ ├── data/
│ │ ├── en/
│ │ │ ├── contraction_expansion/
│ │ │ │ ├── ambiguous_contractions.json: Lists contractions with multiple possible expansions
│ │ │ │ ├── common_stateless_participles.json: Lists common stateless participles
│ │ │ │ ├── idiomatic_phrases.json: Maps idiomatic phrases to their expansions
│ │ │ │ ├── unambiguous_contractions_map.json: Maps each contraction to a single expansion
│ │ │ │ ├── whatcha_are_words.json: Lists words that expand to "are" in "whatcha" expansion
│ │ │ │ └── whatcha_have_words.json: Lists words that expand to "have" in "whatcha" expansion
│ │ │ ├── entity_casing/
│ │ │ │ ├── absolute_casings_map.json: Maps entities that are always capitalized the same way
│ │ │ │ ├── contextual_casings_map.json: Maps entities that require contextto capitalize
│ │ │ │ ├── contraction_suffixes.json: Lists suffixes derived from contractions
│ │ │ │ └── lowercase_particles.json: List of name particles to keep lowercase
│ │ │ ├── string_casing/
│ │ │ │ ├── absolute_casings_map.json: Maps words that are always cased the same way to their cased version
│ │ │ │ ├── lowercase_abbreviations.json: Lists abbreviations that should always be lowercase
│ │ │ │ ├── map_suffix_exceptions.json: Lists suffixes to split off from map-capitalized words
│ │ │ │ ├── prefixed_surnames_map.json: Maps prefixed surnames to their capitalized version
│ │ │ │ ├── surname_prefix_exceptions.json: Lists words that start with surname prefixes but are not surnames
│ │ │ │ └── surname_prefixes.json: Lists common name prefixes
│ │ │ └── elision_words.json: Lists commonly elided words
│ │ └── morse_map.json: Maps characters to their Morse code equivalent
│ ├── providers/
│ │ | ├── en_rules/
│ │ │ ├── __init__.py: Initializes the en_rules sub-package
│ │ │ ├── apostrophes.py: Sets used in English contraction variants
│ │ │ ├── casing.py: English-specific string casing logic
│ │ │ ├── constants.py: English-specific NLP constants
│ │ │ ├── data.py: English-specific data loading and caching
│ │ │ ├── disambiguation.py: Functions for resolving ambiguous contractions based on context
│ │ │ ├── handlers.py: Functions for handling specific types of contractions
│ │ │ ├── regexes.py: English-specific regular expressions
│ │ │ └── utils.py: Utilities for applying casing and finding contraction subjects and verbs
│ │ ├── __init__.py: Strategy pattern classes containing language-specific logic
│ │ ├── base.py: Abstract base class for language providers
│ │ └── en.py: English-specific LanguageProvider implementation
│ ├── __init__.py: Exposes core configuration, constants, and models
│ ├── config.py: A configuration module handling lazy loading of JSON data
│ ├── context.py: Global singleton for the active locale and provider
│ ├── decorators.py: A custom decorator function for non-instantiable classes
│ ├── enums.py: Enumerations for casing, count labels, presence checking and regular expression boundaries
│ ├── exceptions.py: Custom exceptions for clipboard and validation errors
│ ├── models.py: Classes for parts-of-speech counts and word counts
│ ├── types.py: Generic type definitions used across the package
│ └── utils.py: Universal utility functions
├── _lib/
│ ├── casing/
│ │ ├── __init__.py: Exposes casing logic for use across the package
│ │ ├── case_conversion.py: Functions for converting between cases
│ │ ├── entity_casing.py: Function for spaCy-based entity capitalization
│ │ ├── string_casing.py: Function for capitalizing strings through dictionary lookup
│ │ └── token_casing.py: Logic for spaCy-based token capitalization
│ ├── __init__.py: Exposes library functions for use across the package
│ ├── contractions.py: Main logic for expanding contractions
│ ├── encoding.py: Functions for encoding and decoding text
│ ├── manipulation.py: Functions for manipulating a given string
│ ├── nlp.py: Functions for lazy spaCy loading and text processing
│ ├── numbers.py: Functions for converting between cardinal and ordinal numbers
│ └── punctuation.py: Functions for converting between straight and curly quotes
├── locales/
│ └── en/
│   └── LC_MESSAGES/
│     ├── textwarp.mo: Compiled translation machine object file for English
│     └── textwarp.po: Translation source file for English
├── __init__.py: A Python package for analyzing and transforming text
├── __main__.py: The main entry point for the package, containing the main loop and associated functions
├── analysis.py: Public functions for analyzing text
└── warping.py: Public functions for warping text
```

## Usage

Follow these steps to run `textwarp`:

1. **Prerequisites**: Verify that you have Python 3.10 or later. You can install Python at `https://www.python.org/downloads/`. Install Git at `https://git-scm.com/install/`.

2. **Install the package**: Install `textwarp` and its dependencies using pip.

    On macOS/Linux:
    ```
    pip3 install git+https://github.com/adamggrim/textwarp.git
    ```

    On Windows:
    ```
    pip install git+https://github.com/adamggrim/textwarp.git
    ```

3. **Run the program**: Run the program by calling `textwarp` from the command line with a required argument: `textwarp --camel-case`

## License

This project is licensed under the MIT License.

## Contributors

- Adam Grim (@adamggrim)
