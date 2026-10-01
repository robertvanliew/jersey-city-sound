# Read and write data/entries.json without reformatting it.
#
# The file is indent=1, UTF-8 (not ASCII-escaped), CRLF line endings, no trailing
# newline. Writing it any other way turns a one-field edit into a 14,000-line diff.

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRIES = ROOT / "data" / "entries.json"


def load_entries():
    return json.loads(ENTRIES.read_bytes().decode("utf-8"))


def save_entries(data):
    text = json.dumps(data, indent=1, ensure_ascii=False).replace("\n", "\r\n")
    ENTRIES.write_bytes(text.encode("utf-8"))
