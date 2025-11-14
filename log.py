import argparse
from pathlib import Path
from datetime import date, datetime

# Constants
SUCCESS = 0
ERR_DUPLICATE = 1 
ERR_BAD_INPUT = 2 
ERR_IO = 3 
ERR_UNKNOWN = 9

# ---- Helper Functions ----
def get_log_path(filename: str | None = None) -> Path:
    return Path(filename or "log.txt")

def read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]

def write_entry(path: Path, entry: str) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(entry)
        
def format_entry(d: date, note: str) -> str:
    note = (note or "").strip() or "Showed up."
    return f"{d.isoformat()}: {note}\n"

def has_entry(lines: list[str], ymd: str) -> bool:
    prefix = f"{ymd}:"
    return any(ln.startswith(prefix) for ln in lines)

def list_last(lines: list[str], n: int) -> list[str]:
    return lines[-n:] if n > 0 else []


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append a dated note to log.txt or list recent enteries.",
        allow_abbrev=False,
    )

    # With no arguements, applies default (note becomes "showed up")
    parser.add_argument(
        "note",
        nargs="*",
        help="What you did today. If omitted, defaults to 'Showed up.'",
    )
    
    # List most recent N entries 
    parser.add_argument(
        "--list",
        dest="list_count",
        type=int,
        metavar="N",
        help="Show the last N enteries instead of writing a new one.",
    )

    # ----- Options ------
    parser.add_argument(
        "--date",
        dest="on_date",
        metavar="YYYY-MM-DD",
        help="Log for a specific date rather than today.",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow multiple enteries on the same date.",
    )

    parser.add_argument(
        "--prompt",
        action="store_true",
        help="Interactive prompt for the note text.",
    )

    parser.add_argument(
        "--file",
        dest="logfile",
        default="log.txt",
        help="Filepath of the Log (default: log.txt)",
    )
    
    
    return parser.parse_args(argv)

# ---- Orchestration ---- 
def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        log_path = get_log_path(args.logfile)
        lines = read_lines(log_path)

        # LIST mode (no changes to log)
        if args.list_count is not None: 
            if args.list_count <= 0:
                return SUCCESS
            for ln in list_last(lines, args.list_count): 
                print(ln)
            return SUCCESS
        
        # NOTE text (via prompt or argument)
        if args.prompt:
            try: 
                note_text = input("What did you work on today? ").strip()
            except EOFError:
                note_text = ""
        else:
            note_text = " ".join(args.note).strip()

        # DATE 
        if args.on_date:
            try: 
                target_date = datetime.strptime(args.on_date, "%Y-%m-%d").date()
            except ValueError:
                print("Error: --date must be in YYYY-MM-DD format.")
                return ERR_BAD_INPUT
        else:
            target_date = date.today()
        
        ymd = target_date.isoformat()
        
        # DUPLICATE checker 
        if has_entry(lines, ymd) and not args.force:
            print(f"Entry for {ymd} already exists. Use --force to add another.")
            return ERR_DUPLICATE
        
        # WRITE 
        entry = format_entry(target_date, note_text)
        try:
            write_entry(log_path, entry)
        except OSError as e:
            print(f"File error: {e}")
            return ERR_IO
        
        print(f"Logged: {entry.strip()}")
        return SUCCESS
    
    except Exception as e:
        #oh no 
        print(f"Unexpected error: {e}")
        return ERR_UNKNOWN
        

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
