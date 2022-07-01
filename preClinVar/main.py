import logging
from typing import List

import uvicorn
from fastapi import FastAPI, File, UploadFile
from preClinVar.parse import csv_fields_to_submission, csv_lines

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
async def submission_test():
    """Validate a ClinVar submission object by sending a dry run request to the ClinVar API"""
    pass


@app.post("/submission_from_csv")
async def submission_from_csv(files: List[UploadFile] = File(...)):
    """Create and validate a json submission object using one or more CSV files (Variant.csv and CaseData.csv)"""

    # Extract lines from Variants.csv and Casedata.csv files present in POST request
    casedata_lines = None
    variants_lines = None

    for file in files:
        file_lines = await csv_lines(file)
        if "CaseData" in file.filename:
            casedata_lines = file_lines
        else:
            variants_lines = file_lines

    # LOG.debug(f"Variant file contains the following lines:{variants_lines}")
    # LOG.debug(f"CaseData file contains the following lines:{casedata_lines}")

    submission_dict = csv_fields_to_submission(variants_lines, casedata_lines)
    assert submission_dict

    return {"message": "hello"}
