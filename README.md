# Textwarp

`textwarp` is a Python package for manipulating and analyzing clipboard text from the console. For the given clipboard text, `textwarp` applies a conversion or analysis function and copies any modified text to the clipboard.

## Requirements

- Python 3.9

## Dependencies

`textwarp` requires the following Python libraries:

- `pyperclip`: For accessing and copying to the clipboard
- `regex`: For expanded regular expression functionality
- `spaCy`: For identifying parts of speech

## Example

This example demonstrates how to convert text to camel case using `textwarp`.

1. **Copy text to the clipboard**

    In this example, `textwarp` will modify the following clipboard text: `The mind is its own place`.

2. **Run the command**

    Once the text is copied to the clipboard, call `textwarp` from the command line. Enter a required argument for the desired clipboard modification: `textwarp --camel-case`

    For a comprehensive list of `textwarp` arguments, type `textwarp -h` or `textwarp --help`:
    ```
    -h, --help             show this help message and exit
    --alternating-caps     cOnVeRt To AlTeRnAtInG cApS
    --binary               convert to binary
    --camel-case           convertToCamelCase
    --capitalize           Capitalize The First Character Of Each Word
    --cardinal             convert ordinal numbers to cardinal numbers
    --curly-quotes         convert "straight quotes" to “curly quotes”
    --expand-contractions  expand contractions
    --hexadecimal          convert to hexadecimal
    --hyphens-to-em        convert consecutive hyphens to em dashes
    --hyphen-to-en         convert hyphens to en dashes
    --kebab-case           convert-to-kebab-case
    --lowercase            convert to lowercase
    --ordinal              convert cardinal numbers to ordinal numbers
    --pascal-case          ConvertToPascalCase
    --plain-text           convert to plain text
    --punct-to-inside      "move punctuation inside quotation marks."
    --punct-to-outside     "move punctuation outside quotation marks".
    --randomize            randomize the characters in each word
    --redact               redact text
    --reverse              reverse text
    --sentence-case        Convert to sentence case.
    --single-spaces        convert consecutive spaces to a single space
    --snake-case           convert_to_snake_case
    --straight-quotes      convert “curly quotes” to "straight quotes"
    --strikethrough        s̶t̶r̶i̶k̶e̶ ̶t̶h̶r̶o̶u̶g̶h̶ ̶t̶e̶x̶t̶
    --strip                remove leading and trailing whitespace
    --swapcase             convert lowercase to UPPERCASE and vice versa
    --title-case           Convert to Title Case
    --uppercase            CONVERT TO UPPERCASE
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
└── data/
|   └──common_intialisms.json: Lists common initialisms to uppercase
|   └──contraction_tokens.json: Lists contraction tokens split by spaCy
|   └──contractions_map.json: Maps contractions to their expanded versions
|   └──lowercase_particles.json: Lists lowercase particles that should not be capitalized
|   └──morse_map.json: Maps characters to their Morse code equivalents
└── __init__.py: File for recognizing textwarp as a package
├── __main__.py: Runs the textwarp command
├── analyzing.py: Defines functions for analyzing text
├── args.py: Maps command-line arguments to functions and help messages
├── config.py: Loads JSON files for use in the package
├── constants.py: Defines constants used throughout the package
├── enums.py: Defines enum for separator cases
├── input_output.py: Handles user input and console output
├── parsing.py: Parses command-line arguments
├── regexes.py: Defines regular expressions for text parsing
├── setup.py: Loads spaCy model for use in the package
├── validation.py: Defines class and function for clipboard validation
└── warping.py: Defines functions for modifying text
```

## Usage

Follow these steps to run `textwarp`:

1. **Install Python**: Verify that you have Python 3.9 or later. You can install Python at `https://www.python.org/downloads/`.
2. **Review dependencies**: Make sure the required Python packages are installed: `pyperclip`, `spaCy` and `regex`.

    You can check whether these packages are installed using pip's `show` command on each package.

    On macOS:
    ```
    pip3 show spacy
    ```

    If the package is not installed, you will receive a warning: `WARNING: Package(s) not found`. You can install a missing package using pip.

    On macOS:
    ```
    pip3 install spacy
    ```

3. **Install the package**: Install `textwarp` using pip.

    On macOS:

    ```
    pip3 install git+https://github.com/adamggrim/textwarp.git
    ```

4. **Run the program**: Execute the program by calling `textwarp` from the command line with a required argument. For example: `textwarp --camel-case`

## Troubleshooting

If the console cannot find the `textwarp` command when you try to run it from the command line, it was not installed on your system PATH.

To resolve this, follow these steps:

1. Find the installed location of the `textwarp` package using pip's `show` command.

    On macOS:
    ```
    pip3 show textwarp
    ```

    The location of `textwarp` will be listed in the command's output. For example:
    ```
    Location: /Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages
    ```

2. Once you have determined the location of `textwarp`, find the installed location of the `textwarp` command file in your parent Python folder.

    On macOS:
    ```
    find /Library/Frameworks/Python.framework/Versions/3.12/ -name textwarp
    ```

3. Create a symbolic link to the underlying `textwarp` command file and place it in the local directory on your system PATH.

    On macOS:

    ```
    sudo ln -s /Library/Frameworks/Python.framework/Versions/3.12/bin/textwarp /usr/local/bin/
    ```

    To find the system PATH, you can type `echo $PATH` into the console (macOS).

## License

This project is licensed under the MIT License.

## Contributors

- Adam Grim (@adamggrim)
