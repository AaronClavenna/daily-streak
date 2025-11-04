import argparse
from pathlib import Path
from datetime import date, datetime

# Constants
SUCCESS = 0
ERR_DUPLICATE = 1 
ERR_BAD_INPUT = 2 
ERR_IO = 3 
ERR_UNKNOWN = 9



parser = argparse.ArgumentParser(
    description="Append a dated note to log.txt or list recent enteries"
)

parser.add_argument(
    "note",
    nargs="*",
    help="What you did today. If omitted, defaults to 'Showed up.'",
)

parser.add_argument(
    "--date",
    dest="on_date",
    metavar="YYYY-MM-DD",
    help="Log for a specific date rather than today",
)

parser.add_argument(
    "--list",
    dest="list_count",
    type=int,
    metavar="N",
    help="Show the last N enteries instead of writing a new entry",
)

parser.add_argument(
    "--force",
    action="store_true",
    help="Allow multiple enteries on the same date",
)

args = parser.parse_args()

log_path = Path("log.txt")
if not log_path.exists():
    log_path.touch()

text = log_path.read_text(encoding="utf-8")
lines = [ln for ln in text.splitlines() if ln.strip()]

# Handle the "list" action
if args.list_count:
    last = lines[-args.list_count:] if args.list_count > 0 else []
    for ln in last:
        print(ln)
    raise SystemExit(SUCCESS)


# Handle the "date" action
if args.on_date:
    try:
        target_date = datetime.strptime(args.on_date, "%Y-%m-%d").date()
    except ValueError:
        print("Error: --date must be in YYYY-MM-DD format")
        raise SystemExit(ERR_BAD_INPUT)
else:
    target_date = date.today()
    
# Handle the "note" 
note_text = " ".join(args.note).strip()
if not note_text:
    note_text= "Showed up."
    
# Handle not posting the same entry twice in a day, unless on purpose 
prefix = f"{target_date.isoformat()}:"
already = any(ln.startswith(prefix) for ln in lines)

if already and not args.force:
    print(f"Entry for {target_date.isoformat()} already exists. Use --force to add another anyway")
    raise SystemExit(ERR_DUPLICATE)

entry = f"{target_date.isoformat()}: {note_text}\n"

try:
    with log_path.open("a", encoding="utf-8") as f: 
        f.write(entry)
except OSError as e:
    print(f"File error: {e}")
    raise SystemExit(ERR_IO)
    
print(f"Logged: {entry.strip()}")
raise SystemExit(SUCCESS)

