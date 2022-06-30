import logging
from typing import List

import uvicorn
from fastapi import FastAPI, File, UploadFile
from preClinVar.parse import csv_lines

LOG = logging.getLogger("api")
LOG.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
LOG.addHandler(sh)

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

    # Extract lines from Variants.csv and Casedata.csv files present in POST request
    casedata_lines = None
    variants_lines = None

    for file in files:
        file_lines = await csv_lines(file)
        if "CaseData" in file.filename:
            casedata_lines = file_lines
        else:
            variants_lines = file_lines

    LOG.debug(f"Variant file contains the following lines:{variants_lines}")
    LOG.debug(f"Casedata file contains the following lines:{casedata_lines}")

    return {"message": "hello"}
