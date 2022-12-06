DRY_RUN_SUBMISSION_URL = "https://submit.ncbi.nlm.nih.gov/api/v1/submissions/?dry-run=true"
VALIDATE_SUBMISSION_URL = "https://submit.ncbi.nlm.nih.gov/apitest/v1/submissions"

CONDITIONS_MAP = {
    "HPO": "HP",
    "MedGen": "MedGen",
    "MeSH": "MeSH",
    "MONDO": "MONDO",
    "OMIM": "OMIM",
    "Orphanet": "Orphanet",
}

SNV_COORDS = {  # assembly is missing, passed as a request param
    "Chromosome": "chromosome",
    "Start": "start",
    "Stop": "stop",
    "Reference allele": "referenceAllele",
    "Alternate allele": "alternateAllele",
}
SV_COORDS = {  # assembly is missing, passed as a request param
    "Chromosome": "chromosome",
    "Breakpoint 1": "start",
    "Breakpoint 2": "stop",
    "Outer start": "outerStart",
    "Inner start": "innerStart",
    "Inner stop": "innerStop",
    "Outer stop": "outerStop",
}
