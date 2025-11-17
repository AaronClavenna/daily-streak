from pathlib import Path


from log import main, SUCCESS
def test_write_one_line(tmp_path: Path):
    logfile = tmp_path / "log.txt"
    code = main(["--file", str(logfile), "Testing pytest"])
    assert code == SUCCESS
    text = logfile.read_text(encoding="utf-8")
    assert text.count("\n") == 1
    assert "Testing pytest" in text
    
