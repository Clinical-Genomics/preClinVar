import logging
from typing import List

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from preClinVar.parse import csv_fields_to_submission, csv_lines
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
    return {"message": "preClinVar is up and running!"}


@app.get("/submission-test")
async def submission_dryrun():
    """Validate a ClinVar submission object by sending a dry run request to the ClinVar API"""
    pass


@app.post("/csv_2_json")
async def csv_2_json(files: List[UploadFile] = File(...)):
    """Create and validate a json submission object using 2 CSV files (Variant.csv and CaseData.csv)"""

    # Extract lines from Variants.csv and Casedata.csv files present in POST request
    casedata_lines = None
    variants_lines = None

    for file in files:
        file_lines = await csv_lines(file)
        if "CaseData" in file.filename:
            casedata_lines = file_lines
        elif "Variant" in file.filename:
            variants_lines = file_lines

    if not casedata_lines or not variants_lines:
        return JSONResponse(
            status_code=400,
            content={"error": "Both 'Variant' and 'CaseData' csv files are required"},
        )

    # Convert lines extracted from csv files to a submission object (a dictionary)
    submission_dict = csv_fields_to_submission(variants_lines, casedata_lines)

    # Validate submission object using official schema
    valid_results = validate_submission(submission_dict)
    if valid_results[0]:
        return JSONResponse(
            status_code=200,
            content=submission_dict,
        )
    return JSONResponse(
        status_code=400, content={"Created json file contains validation errors": valid_results[1]}
    )
