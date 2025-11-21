from datetime import datetime, timedelta
import os

class DuplicateVisitorError(Exception):
    def __init__(self, visitor_name):
        self.visitor_name = visitor_name
        super().__init__(f"Visitors' {visitor_name}' has already visited.")

class EarlyEntryError(Exception):
    def __init__(self, message="A 5-minute wait is required between different visitors."):
        super().__init__(message)
        
FILENAME = "visitors.txt"

def ensure_file():
    """Create the file if it doesn't exist."""
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as f:
            pass  # create empty file

def get_last_visitor():
    """Return (name, time) of last visitor, or (None, None) if file empty."""
    if not os.path.exists(FILENAME):
        return None, None

    with open(FILENAME, "r") as f:
        lines = f.readlines()
        if not lines:
            return None, None

        last_line = lines[-1].strip()
        if not last_line:
            return None, None

        # Format: name | timestamp
        name, time_str = last_line.split(" | ")
        last_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        return name, last_time

def add_visitor(visitor_name):
    """Add visitor with required checks."""
    last_name, last_time = get_last_visitor()
    
    now = datetime.now()

    # Rule 1: No duplicate consecutive visitors
    if last_name == visitor_name:
        raise DuplicateVisitorError(visitor_name)

    # Append to file
    with open(FILENAME, "a") as f:
        f.write(f"{visitor_name} | {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
  
def main():
    ensure_file()
    name = input("Enter visitor's name: ")

    try:
        add_visitor(name)
        print("Visitor added successfully!")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()