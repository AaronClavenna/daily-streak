from pathlib import Path
import pytest 

from log import main, SUCCESS
def test_write_one_line(tmp_path: Path):
    logfile = tmp_path / "log.txt"
    code = main(["--file", str(logfile), "Testing pytest"])
    assert code == SUCCESS
    text = logfile.read_text(encoding="utf-8")
    assert text.count("\n") == 1
    assert "Testing pytest" in text
    
from log import main, ERR_DUPLICATE
def test_duplicate_blocked(tmp_path: Path):
    logfile = tmp_path / "log.txt"
    _ = main(["--file", str(logfile), "First note"])
    code = main(["--file", str(logfile), "Second note"])
    assert code == ERR_DUPLICATE
    lines = logfile.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    
from log import main, SUCCESS
def test_list_mode_on_empty_file(tmp_path, capsys):
    logfile = tmp_path / "log.txt"
    code = main(["--file", str(logfile), "--list", "5"])
    out = capsys.readouterr().out
    assert code == SUCCESS
    assert out == "" #there should be nothing listed yet 
    
from log import main, ERR_BAD_INPUT
@pytest.mark.parametrize("bad", ["2025/11/18", "11-18-2025", "2025-13-01", "abc"])
def test_bad_dates_rejected(tmp_path, bad):
    logfile = tmp_path / "log.txt"
    code = main(["--file", str(logfile), "--date", bad, "x"])
    assert code == ERR_BAD_INPUT
    
from log import main, SUCCESS
def test_force_allows_second_entry(tmp_path):
    logfile = tmp_path / "log.txt"
    assert main(["--file", str(logfile), "first"]) == SUCCESS
    assert main(["--file", str(logfile), "--force", "second"]) == SUCCESS
    lines = logfile.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    
