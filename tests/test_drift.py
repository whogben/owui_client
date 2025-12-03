import pytest
import sys
from pathlib import Path

# Add scripts directory to path
# test file is at owui_client/tests/test_drift.py
# scripts is at owui_client/scripts
scripts_dir = Path(__file__).parents[1] / "scripts"
sys.path.append(str(scripts_dir))

from check_drift import find_drift

def test_drift_check():
    """
    Checks if there is any drift between the Open WebUI backend reference and our client.
    This test will fail if:
    1. Implemented models are missing fields present in the backend.
    2. Implemented routers are missing endpoints present in the backend.
    """
    issues = find_drift()
    
    if issues:
        # Format issues for failure message
        message = f"Found {len(issues)} drift issues:\n" + "\n".join([str(i) for i in issues])
        pytest.fail(message)
