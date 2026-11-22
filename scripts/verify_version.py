import json
import sys
from urllib.request import urlopen

expected_version = sys.argv[1]

with urlopen("http://127.0.0.1:8000/version", timeout=5) as response:
    data = json.load(response)

actual_version = data.get("version")

if actual_version != expected_version:
    raise SystemExit(
        f"Version mismatch: expected {expected_version}, got {actual_version}"
    )

print(f"Version verified: {actual_version}")