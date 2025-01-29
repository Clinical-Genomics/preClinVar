SUBMISSION_URL = "https://submit.ncbi.nlm.nih.gov/api/v1/submissions"
DRY_RUN_SUBMISSION_URL = f"{SUBMISSION_URL}/?dry-run=true"
VALIDATE_SUBMISSION_URL = "https://submit.ncbi.nlm.nih.gov/apitest/v1/submissions"

CLNSIG_TERMS = [
    "Pathogenic",
    "Likely pathogenic",
    "Uncertain significance",
    "Likely benign",
    "Benign",
    "Pathogenic, low penetrance",
    "Uncertain risk allele",
    "Likely pathogenic, low penetrance",
    "Established risk allele",
    "Likely risk allele",
    "affects",
    "association",
    "drug response",
    "confers sensitivity",
    "protective",
    "other",
    "not provided",
]

CONDITIONS_MAP = {
    "HPO": "HP",
    "MedGen": "MedGen",
    "MeSH": "MeSH",
    "MONDO": "MONDO",
    "OMIM": "OMIM",
    "Orphanet": "Orphanet",
}

SNV_COORDS = {  # assembly is missing, passed as a request param
    "Chromosome": {"key": "chromosome", "format": str},
    "Start": {"key": "start", "format": int},
    "Stop": {"key": "stop", "format": int},
    "Reference allele": {"key": "referenceAllele", "format": str},
    "Alternate allele": {"key": "alternateAllele", "format": str},
}
SV_COORDS = {  # assembly is missing, passed as a request param
    "Chromosome": {"key": "chromosome", "format": str},
    "Breakpoint 1": {"key": "start", "format": int},
    "Breakpoint 2": {"key": "stop", "format": int},
    "Outer start": {"key": "outerStart", "format": int},
    "Inner start": {"key": "innerStart", "format": int},
    "Inner stop": {"key": "innerStop", "format": int},
    "Outer stop": {"key": "outerStop", "format": int},
}
