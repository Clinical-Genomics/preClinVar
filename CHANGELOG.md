## [unreleased]
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
### Changed
- Updated submission schema in resources following new release of schema by ClinVar (draft-07)
- Improved README files with description of endpoints and how to test it
### Fixed
- Parsing of CaseData csv with more than one individuals associated to the same variant
- dry-run enpoint, to return success when ClinVar returns a 204 successful response
