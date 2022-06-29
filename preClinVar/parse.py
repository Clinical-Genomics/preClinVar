import logging
import os
from csv import DictReader
from tempfile import NamedTemporaryFile

LOG = logging.getLogger(__name__)


async def csv_lines(csv_file):
    """Extracts header and file lines from a csv file

    Args:
        csv_file(starlette.datastructures.UploadFile)
    Returns:
        lines(list of dictionaries). Example [{'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH'}, ..]
    """

    contents = await csv_file.read()
    file_copy = NamedTemporaryFile(delete=False)
    lines = []
    try:
        with file_copy as f:
            f.write(contents)

        with open(file_copy.name, "r", encoding="utf-8") as csvf:
            csvreader = DictReader(csvf)
            next(csvreader)  # skip header
            for row in csvreader:
                lines.append(row)

    finally:
        file_copy.close()  # Close temp file
        os.unlink(file_copy.name)  # Delete temp file

    return lines
