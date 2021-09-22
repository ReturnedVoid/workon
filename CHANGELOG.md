# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased


## [1.0.0] - 2021-07-31
### Added
* Simple bash completions
* Better logging for `start` command
* Small README.md improvements

### Changed
* Install user config file manually in "setup.py"

## [0.3.0] - 2021-07-26
### Removed
* `open` command
* `errors.py` module. Now all script exceptions live inside `script.py` module

### Changed
* `start` command now opens a project if it exists
* Default logging level is INFO (was ERROR before). Logging generally improved

## [0.2.1] - 2021-06-23
### Fixed
* `done` command: also remove named pipes and symbolic links

### Added
* Describe how to run integration tests
* Show detailed information about left stashes

## [0.2.0] - 2021-06-05
### Changed
* Use configuration file instead of environment variables

## [0.1.0] - 2021-05-13
### Added
* Tests coverage target to Makefile
* `open` command description
* Improve force logs for `done` command

### Fixed
* Made some unit tests to be environment-agnostic

### Changed
* Remove `-f/--force` flag from `start` command. Allow multiple projects

## [0.0.4] - 2021-05-08
### Added
* `done` command now also removes files
* `done` command now really tries to remove all projects
* `open` command for opening already started projects

### Fixed
* Correctly handle exception raised when specified editor does not exist

## [0.0.3] - 2021-05-06
### Added
* `done` command now also checks unstaged changes

### Fixed
* Add `--no-open` flag to integration tests to prevent unwanted opens

## [0.0.2] - 2021-05-06
### Added
* `start` command: open cloned project in a specified editor
  * `-e/--editor` and `-n/--no-open` arguments

### Fixed
* Small script help fixes/improvements

## [0.0.1] - 2021-05-05
### Added
* Initial tested version