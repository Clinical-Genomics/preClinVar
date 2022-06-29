import logging
from typing import List

LOG = logging.getLogger(__name__)
from fastapi import FastAPI, File, UploadFile
from preClinVar.parse import csv_header_lines

app = FastAPI()


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

    # Extract header and lines from files present in POST request
    variants_csv = None
    casedata_csv = None

    for file in files:
        file_lines = await csv_header_lines(file)
        if "CaseData" in file.filename:
            casedata_csv = file_lines
        else:
            variants_csv = file_lines

    LOG.warning(casedata_csv)
    LOG.error(variants_csv)

    return {"message": "hello"}
