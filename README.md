# PreClinVar
A ClinVar API submission helper written in FastAPI.

## Available endpoints:

### csv_2_json

Transforms csv submission files (Variant.csv and CaseData.csv) into a json submission object, ready to be used to submit via the ClinVar API. This document is validated against the ClinVar API [submission schema](https://www.ncbi.nlm.nih.gov/clinvar/docs/api_http/)

### dry_run

Proxy endpoint to the ClinVar submissions API (dry-run): https://submit.ncbi.nlm.nih.gov/api/v1/submissions/?dry-run=true. Requires a valid API key and a json file containing a submission object. If the request is valid (and the json submission object is validated) returns a submission ID which can be used for a real submission.

### validate

Proxy endpoint to the ClinVar validate API endpoint: "https://submit.ncbi.nlm.nih.gov/apitest/v1/submissions". Requires a valid API key and a json file containing a submission object. If the json submission document is valid returns a submission ID which can be used for a real submission. If the json submission document is not validated, the endpoint returns a list of errors which will help fixing the document.

## Running the application using Docker-compose
An example containing a demo setup for the app is included in the docker-compose file. Start the docker-compose demo using this command:
```
docker-compose up -d
```
The server will be running and accepting requests sent from outside the container (another terminal or a web browser) on port <strong>7000</strong> (http://0.0.0.0:7000)


## Installing the application on a local conda environment

Given a conda environment sontaining python 3.8 and [poetry](https://github.com/python-poetry/poetry), clone the repository from Github with the following command:

```
git clone https://github.com/Clinical-Genomics/preClinVar.git
```

The command will create a folder named `preClinVar` in your current working directory. Move inside this directory:

```
cd preClinVar
```

And install the software with poetry:

```
poetry install
```

You can run an instance of the server by typing:

```
uvicorn preClinVar.main:app --reload --log-level debug
```

The server will run on localhost and default port 8000 (http://127.0.0.1:8000)


## Testing the endpoints

The endpoints will be available under the docs: http://127.0.0.1:8000/docs (http://127.0.0.1:7000/docs if you are running the dockerized version of the app).
They can be tested with files provided in this repository, in the demo folder: https://github.com/Clinical-Genomics/preClinVar/tree/main/preClinVar/demo
