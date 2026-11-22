"""
download_data.py

What: Downloads the 3 Lending Club files from Kaggle into data/download/.
Why:  A script makes the download repeatable. It skips files that are already
      complete, so it is safe to run again (idempotent).
Run:  python ingestion/download_data.py   (from the project folder, with .venv active)
"""

import logging
import os
import shutil
import subprocess
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

# This file lives in ingestion/, so the project folder is one level up.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOWNLOAD_DIR = PROJECT_ROOT / "data" / "download"

# (Kaggle dataset, file name, expected size in bytes).
# Sizes come from `kaggle datasets files` (Step 0.7). A different size means
# the download stopped early, or Kaggle changed the file.
FILES_TO_DOWNLOAD = [
    ("ethon0426/lending-club-20072020q1", "LCDataDictionary.xlsx", 18_440),
    ("wordsforthewise/lending-club", "rejected_2007_to_2018Q4.csv.gz", 255_470_782),
    ("ethon0426/lending-club-20072020q1", "Loan_status_2007-2020Q3.gzip", 1_773_470_505),
]

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
logger = logging.getLogger(__name__)


def is_complete(file_path: Path, expected_size: int) -> bool:
    """Return True if the file exists and has exactly the expected size."""
    return file_path.exists() and file_path.stat().st_size == expected_size


def download_file(dataset: str, file_name: str, expected_size: int) -> None:
    """Download one file from Kaggle into DOWNLOAD_DIR, unless it is already complete.

    Raises RuntimeError if the file has the wrong size after downloading.
    """
    target_file = DOWNLOAD_DIR / file_name

    if is_complete(target_file, expected_size):
        logger.info("Skip %s: already downloaded", file_name)
        return

    logger.info("Downloading %s from %s ...", file_name, dataset)
    subprocess.run(
        [
            "kaggle", "datasets", "download", dataset,
            "-f", file_name,
            "-p", str(DOWNLOAD_DIR),
            # Kaggle sends big files inside a .zip. --unzip unpacks them to the normal name.
            "--unzip",
        ],
        check=True,  # stop the script if Kaggle reports an error
    )

    if not is_complete(target_file, expected_size):
        actual_size = target_file.stat().st_size if target_file.exists() else 0
        raise RuntimeError(
            f"{file_name}: expected {expected_size:,} bytes but found {actual_size:,}. "
            "If the download stopped early, run the script again to resume it."
        )
    logger.info("Done %s (%s bytes)", file_name, f"{expected_size:,}")


def main() -> None:
    """Load the Kaggle token, then download every file in FILES_TO_DOWNLOAD."""
    load_dotenv(PROJECT_ROOT / ".env")  # puts KAGGLE_API_TOKEN into this program's settings

    # Stop early with a clear message, instead of a confusing Kaggle error later.
    if not os.getenv("KAGGLE_API_TOKEN"):
        raise SystemExit("KAGGLE_API_TOKEN is missing. Add it to the .env file.")
    if shutil.which("kaggle") is None:
        raise SystemExit("Kaggle CLI not found. Activate .venv first: .\\.venv\\Scripts\\Activate.ps1")

    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    for dataset, file_name, expected_size in FILES_TO_DOWNLOAD:
        download_file(dataset, file_name, expected_size)
    logger.info("All %d files are ready in %s", len(FILES_TO_DOWNLOAD), DOWNLOAD_DIR)


if __name__ == "__main__":
    main()