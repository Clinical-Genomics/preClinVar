import json
import logging
import re
from typing import List

import requests
import uvicorn
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import JSONResponse

from preClinVar.__version__ import VERSION
from preClinVar.build import build_header, build_submission
from preClinVar.constants import DRY_RUN_SUBMISSION_URL, VALIDATE_SUBMISSION_URL
from preClinVar.file_parser import csv_lines, file_fields_to_submission, tsv_lines
from preClinVar.validate import validate_submission

LOG = logging.getLogger("uvicorn.access")

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    LOG = logging.getLogger("uvicorn.access")
    console_formatter = uvicorn.logging.ColourizedFormatter(
        "{levelprefix} {asctime} : {message}", style="{", use_colors=True
    )
    LOG.handlers[0].setFormatter(console_formatter)


@app.get("/")
async def root():
    return {"message": f"preClinVar v{VERSION} is up and running!"}


@app.post("/apitest-status")
async def apitest_status(api_key: str = Form(), submission_id: str = Form()) -> JSONResponse:
    """Returns the status (validation) of a test submission to the apitest endpoint."""

    # Create a submission header
    header = build_header(api_key)

    apitest_actions_url = f"{VALIDATE_SUBMISSION_URL}/{submission_id}/actions/"
    apitest_actions_resp = requests.get(apitest_actions_url, headers=header)

    return JSONResponse(
        status_code=apitest_actions_resp.status_code,
        content=apitest_actions_resp.json(),
    )


@app.post("/apitest")
async def apitest(api_key: str = Form(), json_file: UploadFile = File(...)):
    """A proxy to the apitest ClinVar API endpoint"""
    # Create a submission header
    header = build_header(api_key)

    # Get json file content as dict:
    submission_obj = json.load(json_file.file)

    # And use it in POST request to API
    data = {
        "actions": [
            {
                "type": "AddData",
                "targetDb": "clinvar",
                "data": {"content": submission_obj},
            }
        ]
    }
    resp = requests.post(VALIDATE_SUBMISSION_URL, data=json.dumps(data), headers=header)
    return JSONResponse(
        status_code=resp.status_code,
        content=resp.json(),
    )


@app.post("/dry-run")
async def dry_run(api_key: str = Form(), json_file: UploadFile = File(...)):
    """A proxy to the dry run submission ClinVar API endpoint"""
    # Create a submission header
    header = build_header(api_key)

    # Get json file content as dict:
    submission_obj = json.load(json_file.file)

    # And use it in POST request to API
    data = {
        "actions": [
            {
                "type": "AddData",
                "targetDb": "clinvar",
                "data": {"content": submission_obj},
            }
        ]
    }
    resp = requests.post(DRY_RUN_SUBMISSION_URL, data=json.dumps(data), headers=header)

    # A successful response will be an empty response with code 204 (A dry-run submission was successful and no submission was created)
    if resp.status_code == 204:
        return JSONResponse(
            status_code=200,
            content={"message": "success"},
        )
    return JSONResponse(
        status_code=resp.status_code,
        content=resp.json(),
    )


@app.post("/tsv_2_json")
async def tsv_2_json(
    request: Request,
    files: List[UploadFile] = File(...),
):
    """Create a json submission object using 2 TSV files (Variant.tsv and CaseData.tsv).
    Validate the submission objects against the official schema:
    https://www.ncbi.nlm.nih.gov/clinvar/docs/api_http/
    """
    # Extract lines from Variants.tsv and Casedata.tsv files present in POST request
    casedata_lines = None
    variants_lines = None

    for file in files:
        file_lines = await tsv_lines(file)
        if not file_lines:
            return JSONResponse(
                status_code=400,
                content={"message": f"Malformed file {file.filename}"},
            )

        if re.search("CaseData", file.filename, re.IGNORECASE):
            casedata_lines = file_lines
        elif re.search("Variant", file.filename, re.IGNORECASE):
            variants_lines = file_lines

    # Make sure both files were provided in request
    if not casedata_lines or not variants_lines:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Both 'Variant' and 'CaseData' tsv files are required and should not be empty"
            },
        )

    # Convert lines extracted from csv files to a submission object (a dictionary)
    submission_dict = file_fields_to_submission(variants_lines, casedata_lines)
    build_submission(submission_dict, request)

    # Validate submission object using official schema
    valid_results = validate_submission(submission_dict)
    if valid_results[0]:
        return JSONResponse(
            status_code=200,
            content=submission_dict,
        )
    return JSONResponse(
        status_code=400,
        content={"message": f"Created json file contains validation errors: {valid_results[1]}"},
    )


@app.post("/csv_2_json")
async def csv_2_json(
    request: Request,
    files: List[UploadFile] = File(...),
):
    """Create a json submission object using 2 CSV files (Variant.csv and CaseData.csv).
    Validate the submission objects agains the official schema:
    https://www.ncbi.nlm.nih.gov/clinvar/docs/api_http/
    """

    # Extract lines from Variants.csv and Casedata.csv files present in POST request
    casedata_lines = None
    variants_lines = None

    for file in files:
        file_lines = await csv_lines(file)
        if not file_lines:
            return JSONResponse(
                status_code=400,
                content={"message": f"Malformed file {file.filename}"},
            )

        if re.search("CaseData", file.filename, re.IGNORECASE):
            casedata_lines = file_lines
        elif re.search("Variant", file.filename, re.IGNORECASE):
            variants_lines = file_lines

    # Make sure both files were provided in request
    if not casedata_lines or not variants_lines:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Both 'Variant' and 'CaseData' csv files are required and should not be empty"
            },
        )

    # Convert lines extracted from csv files to a submission object (a dictionary)
    try:
        submission_dict = file_fields_to_submission(variants_lines, casedata_lines)
        build_submission(submission_dict, request)
    except Exception as ex:
        return JSONResponse(
            status_code=400,
            content={"message": str(ex)},
        )

    # Validate submission object using official schema
    valid_results = validate_submission(submission_dict)
    if valid_results[0]:
        return JSONResponse(
            status_code=200,
            content=submission_dict,
        )
    return JSONResponse(
        status_code=400,
        content={"message": f"Created json file contains validation errors: {valid_results[1]}"},
    )
