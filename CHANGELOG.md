## [2.3.1]
### Fixed
- Combine `Reference sequence` and `HGVS` fields from Variant file to create the hgvs field in json submission object

## [2.3]
### Changed
- Fix uppercase/lowercase letters when parsing clinsig terms from files

## [2.2]
### Changed
- Provide the URL to the prod service running on the Clinical Genomics server instead of the stage one on README page
### Fixed
- Do not parse dbSNP IDs as `Accession` key/values

## [2.1]
### Added
- Parsing of `variantType`, `referenceCopyNumber`, `copyNumber` and `chromosomeCoordinates` fields from CSV/TSV files
- Genome assembly can be passed as an optional param to tsv_2_json and csv_to_json to create submission containing chromosome coordinates
- Link to demo service instance at clinical genomics
### Fixed
- Parsing of multiple condition IDs from csv/tsv files

## [2.0.1]
### Fixed
- Parsing of `Condition ID type`
- Do not include HGVS field in submission if it is null

## [2.0]
### Added
- A new tsv_2_json endpoint to convert TSV files in json submission objects
- `Keep a Changelog` GitHub action
- `Black` GitHub action
- `Flake8 Lint` GitHub action
- `Vulture` GitHub action
- `Woke` GitHub action
- Badges showing the status of GitHub actions on README page
- File conversion endpoints accept optional parameters to set the following key/values: `submissionName, clinvarSubmissionReleaseStatus, assertionCriteria`
### Changed
- New API schema introduced on 2022-11-21
- Modified file parsing code to create submission jsons compliant with the new API
- Renamed the old demo CSV files to FILENAME_before_221121.csv
- Demo json submission file to include `submissionName` and `clinvarSubmissionReleaseStatus` key/values
### Fixed
- Do not crash when parsing Variant CSV files with no assertion criteria
- Simplify and fix CSV and TSV files parsing

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
