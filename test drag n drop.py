
import sys

# check if file was dropped on the script
if len(sys.argv) < 2:
    print("Drag and drop a file onto this script.")
    input("Press Enter to exit...")
    exit()

# this is the file you dropped
input_file = sys.argv[1]

print("Loaded file:", input_file)
print("Reading lines...\n")

# open and read the file line by line
with open(input_file, "r") as f:
    for line in f:
        line = line.strip()
        print(line)

input("\nDone. Press Enter to close...")