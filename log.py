import sys
note = " ".join(sys.argv[1:])

from datetime import date
today = date.today().isoformat()

entry = f"{today}: {note}\n"

with open("log.txt", "a") as file:
    file.write(entry)
    
print(f"Logged: {entry.strip()}")
