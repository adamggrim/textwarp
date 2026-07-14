# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
* Logarithmically accelerating spinner for spaCy commands.
* New `--debug` argument.

### Changed
* Improved error handling.
* Introduced a half-second input delay for "Any other text?" prompts.
* Allowed early exit from integer prompts.
* Expanded internationalization support.
* Fixed analysis output to file.
* Fixed a bug where Pascal and camel casing overrode separator cases for known initialisms.
* Split some larger files to adhere to single-responsibility principle.
* Updated pipeline handling of intermediate and replacement inputs.
* Wrapped words in single quotes for MFWs analysis.
* Added apostrophe-based suffix support for initialisms.
* Improved token type classification during text normalization.

### Internal
* Updated tests to reflect the new spinner, input delay, early exit and MFWs formatting.
* Added affirmative inputs test.
* Updated test strings.
* Renamed `to_verb_words.json` to `infinitive_exceptions.json`.
