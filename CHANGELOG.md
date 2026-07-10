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
* Wrapped words in single quotes for MFWs analysis.

### Internal
* Updated tests to reflect the new spinner, input delay, early exit and MFWs formatting.
* Added affirmative inputs test.
* Updated test strings.
