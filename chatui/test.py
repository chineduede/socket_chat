import sys
import os

def set_scrolling_region(line0=None, line1=None):
    if line0 == None:
        return "\x1b[r"

    if line1 is None:
        line1 = line0
        line0 = 1

    return f"\x1b[{line0};{line1}r"

def save_cursor():
    sys.stdout.write("\x1b7")

def restore_cursor():
    sys.stdout.write("\x1b8")

def move_cursor(row, col):
    sys.stdout.write(f"\x1b[{row};{col}r")

# Save current cursor position

set_scrolling_region(9)
while True:
    print("Hello, world!")

# Now, you're back where you started
