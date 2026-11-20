from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_required_project_files_exist():
    for relative in ("main.py", "requirements.txt", "buildozer.spec", "README.md"):
        assert (ROOT / relative).is_file()
