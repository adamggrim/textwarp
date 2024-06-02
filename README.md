# Textwarp

`textwarp` is a Python package for modifying clipboard text from the console. For the given clipboard text, `textwarp` applies a conversion function and copies the modified text to the clipboard.

## Requirements

- Python 3.6

## Dependencies

`textwarp` requires the following Python libraries:

- `nltk`: For identifying parts of speech to capitalize for title case
- `pyperclip`: For accessing and copying to the clipboard
- `setuptools`: For building and installing the `textwarp` package, and for implementing command-line functionality using entry points

## Examples

This example demonstrates how to convert text to camel case using `textwarp`.

1. **Copy text to the clipboard**

    In this example, `textwarp` will modify the following clipboard text: `The mind is its own place`

2. **Run the command**

    Once the text is copied to the clipboard, call `textwarp` from the command line. Enter a required argument for the desired clipboard modification: `textwarp --camel-case`

    For a list of `textwarp` arguments, type `textwarp -h` or `textwarp --help`:
    ```
    -h, --help           show this help message and exit
    --camel-case         convert to camel case
    --capitalize         capitalize the first character of each word
    --curly-to-straight  convert curly quotes to straight quotes
    --hyphens-to-em      convert consecutive hyphens to em dashes
    --hyphen-to-en       convert hyphens to en dashes
    --kebab-case         convert to kebab case
    --lowercase          convert to lowercase
    --pascal-case        convert to Pascal case
    --punct-to-inside    move punctuation inside quotation marks
    --punct-to-outside   move punctuation outside quotation marks
    --snake-case         convert to snake case
    --straight-to-curly  convert straight quotes to curly quotes
    --title-case         convert to title case
    --uppercase          convert to uppercase
    ```

3. **Paste text from the clipboard**

    `textwarp` will copy the modified text to the clipboard: `theMindIsItsOwnPlace`. Paste to view the mosified text.

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
└── __init__.py: File for recognizing textwarp as a package
├── __main__.py: File for running the textwarp command
├── constants.py: Defines constants used throughout the package
├── enums.py: Defines enum for separator cases
├── input_output.py: Handles user input and console output
├── parsing.py: Parses command-line arguments
├── regexes.py: Defines regular expressions for text parsing
└── warping.py: Defines functions for modifying text
```

## Usage

Follow these steps to run `textwarp`:

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