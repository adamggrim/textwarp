# Textcount

`textcount` is a Python package for analyzing clipboard text from the console. For the given clipboard text, `textcount` applies an analysis function and prints the analysis to the console.

## Requirements

- Python 3.6

## Dependencies

`textcount` requires the following Python libraries:

- `nltk`: For counting words and parts of speech
- `pyperclip`: For accessing clipboard text
- `setuptools`: For building and installing the `textcount` package, and for implementing command-line functionality using entry points

## Examples

This example demonstrates how to print a parts-of-speech count using `textcount`.

1. **Copy text to the clipboard**

    In this example, `textcount` will count parts of speech for the following clipboard text: `The apparition of these faces in the crowd: Petals on a wet, black bough.`

2. **Run the command**

    Once the text is copied to the clipboard, call `textcount` from the command line. Enter a required argument for the desired clipboard analysis: `textcount --pos-count`

    For a list of `textcount` arguments, type `textcount -h` or `textcount --help`:
    ```
    -h, --help           show this help message and exit
    --char-count         print the number of characters
    --mfws               print the most frequent words
    --pos-count          print the count for each part of speech
    --time-to-read       print the time to read at a given reading speed
    --word-count         print the word count
    ```

3. **Print the analysis**

    `textcount` will print the selected analysis to the clipboard:

    ```
    Adjectives:    2 (14.29%)
    Adpositions:   3 (21.43%)
    Adverbs:         0 (0.0%)
    Conjunctions:    0 (0.0%)
    Determiners:   4 (28.57%)
    Nouns:         5 (35.71%)
    Particles:       0 (0.0%)
    Pronouns:        0 (0.0%)
    Verbs:           0 (0.0%)
    Other:           0 (0.0%)
    ```

4. **Continue or exit**

    The program will prompt you to copy any other text to the clipboard. To exit, type `no` (`n`), `quit` (`q`) or `exit` (`e`), or trigger a KeyboardInterrupt (Ctrl + C):

    ```
    Any other text? (y/n) (Copy text to clipboard):
    ^C

    Exiting the program...
    ```

## Structure

```
textcount/
└── __init__.py: File for recognizing textcount as a package
├── __main__.py: File for running the textcount command
├── analyzing.py: Defines functions for text analysis
├── constants.py: Defines constants used throughout the package
├── data_structures.py: Defines data structures used throughout the package
├── formatting.py: Defines functions for formatting text analysis
├── input_output.py: Handles user input and console output
├── parsing.py: Parses command-line arguments
└── regexes.py: Defines regular expressions for text cleaning
```

## Usage

Follow these steps to run `textcount`:

1. **Install Python**: Verify that you have Python 3.6 or later. You can install Python at `https://www.python.org/downloads/`.
2. **Review dependencies**: Make sure the required Python packages are installed: `nltk`, `pyperclip` and `setuptools`.

    You can check whether these packages are installed using pip's `show` command on each package.

    On macOS:
    ```
    pip3 show nltk
    ```

    If the package is not installed, you will receive the warning, `WARNING: Package(s) not found`. You can install a missing package using pip.

    On macOS:
    ```
    pip3 install nltk
    ```

3. **Install the package**: Install `textcount` using pip.

    On macOS:

    ```
    pip3 install git+https://github.com/adamggrim/textcount.git
    ```

4. **Run the program**: Execute the program by calling `textcount` from the command line with a required argument. For example: `textcount --pos-count`

## Troubleshooting

If the console cannot find the `textcount` command when you try to run it from the command line, it was not installed on your system PATH.

To resolve this, follow these steps:

1. Find the installed location of the `textcount` package using pip's `show` command.

    On macOS:
    ```
    pip3 show textcount
    ```

    The location of `textcount` will be listed in the command's output. For example:
    ```
    Location: /Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages
    ```

2. Once you have determined the location of `textcount`, find the installed location of the `textcount` command file in your parent Python folder.

    On macOS:
    ```
    find /Library/Frameworks/Python.framework/Versions/3.12/ -name textcount
    ```

3. Create a symbolic link to the underlying `textcount` command file and place it in the local directory on your system PATH.

    On macOS:

    ```
    sudo ln -s /Library/Frameworks/Python.framework/Versions/3.12/bin/textcount /usr/local/bin/
    ```

    To find the system PATH, you can type `echo $PATH` into the console (macOS).

## License

This project is licensed under the MIT License.

## Contributors

- Adam Grim (@adamggrim)