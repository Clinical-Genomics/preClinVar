## [unreleased]
### Added
- `validate` endpoint, supporting validation of germline or somatic json submission against their respective schema
### Changed
- Improve README and endpoint descriptions specifying that `tsv_2_json` and `csv_2_json` endpoints support only coversion for germline submission files
- PR template to be more compact and user friendly
### Fixed
- GitHub action to use poetry v.1.7.1

## [2.7.1]
### Fixed
- Replace the CMD step of the Dockerfile with an ENTRYPOINT that uses `/bin/sh -c` to evaluates the shell commands and expand environment variables.

## [2.7]
### Added
- Delete submission endpoint, with json example (under demo files) and test
### Changed
- Updated API submission schema to the latest available on `ncbi/clinvar` GitHub pages
- Modified the json submission example to use one from the ClinVar GitHib repo (`sample_clinical_significance_hgvs_submission.json`)
- Removed the example of an old json submission (before 2022-11-21) 
- Updated actions using the latest base images and to run using Python 3.9
- Docker image uses Python 3.11 instead of 3.8
- Replaced deprecated app "on event" with app lifespan
### Fixed
- Updated issue templates
- Updated a number of libraries to address all current security advisories
- Warnings in the Dockerfile

## [2.6]
### Added
- An endpoint `/apitest-status` that returns a response containing the status of a test submission, with link to the eventual json file with the submissions data errors
- An endpoint `/status` that returns a response containing the status of a submission (submitted, processing, processed, error), with eventual error details
### Changed
- Renamed `/validate` endpoint to `/apitest`

## [2.5.2]
### Fixed
- Upload to Codecov step in `tests_n_coverage.yml` action
- Fix `multipleConditionExplanation` to be lowercase

## [2.5.1]
### Fixed
- Avoid "/bin/sh: 1: gunicorn: not found" error by using poetry <1.8 in Dockerfile

## [2.5]
### Changed
- Updated submission schema to the latest API schema (01-03-2024)
- Switched from Draft3Validator to Draft7Validator in validate.py
- Updated fastapi lib to fix security vulnerability
- Parse `conditionSet.MultipleConditionExplanation` value from `Explanation for multiple conditions` column of variants file

## [2.4]
### Changed
- Updated version of external images in GitHub actions
- Updated API submission schema to the latest
- Demo variant to take care of "Somatic mutation" no longer available among Mode of inheritance choices
- `clinicalSignificance.clinicalSignificanceDescription` value extracted from `Clinical significance` or `Germline classification` column
- `clinicalSignificance.comment` values extracted from `Comment on clinical significance` or `Comment on classification` column
### Fixed
- Bump certifi from 2022.12.7 to 2023.7.22
- Description of the response returned by dry run endpoint in README file
- Migrate from deprecated `pkg_resources` lib to `importlib_resources`
- Updated python-multipart from 0.0.5 to 0.0.7 to address security alert by dependabot

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
