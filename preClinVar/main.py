from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "preClinVar is up and running!"}


@app.get("/submission-test")
async def submission_test():
    """Validate a ClinVar submission object by sending a dry run request to the ClinVar API"""
    pass
