## [unreleased]
### Fixed
- Do not crash when parsing Variant CSV files with no assertion criteria

## [1.0.2]
### Fixed
- Prevent CSV file parsing StopIteration error when provided files are empty

## [1.0.1]
### Fixed
- Fixed Dockerfile building error resulting in prod image release failed to be pushed to Docker Hub

## [1.0]
### Added
- Poetry install
- main.py file with first functions
- .gitignore and CHANGELOG files
- json submission_schema and demo submission object
- tests folder
- Basic howto on README.md
- submission_from_csv endpoint and function to read csv files
- Add custom logging formatting
- Tests and coverage GitHub workflow
- Proxy endpoint to interrogate the submission dry run endpoint of ClinVar API
- Proxy endpoint to interrogate the submission validate endpoint of ClinVar API
- Dockerfile
- Docker-compose file
- GitHub actions to build Docker images (prod and stage) and push them to Docker Hub
- Codecov coverage badge
### Changed
- Updated submission schema in resources following new release of schema by ClinVar (draft-07)
- Improved README files with description of endpoints and how to test it
- Increased test coverage
- Pass ClinVar API KEY as a form field and not a query argument
### Fixed
- Parsing of CaseData csv with more than one individuals associated to the same variant
- dry-run enpoint, to return success when ClinVar returns a 204 successful response
- Dockerfile returning `__call__() missing 1 required positional argument: 'send' error`
