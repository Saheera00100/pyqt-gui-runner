# demo_script.py

import sys

def main():
    with open("output_log.txt", "w") as f:
        f.write("Received arguments:\n")
        for arg in sys.argv[1:]:  # Skip the first one (filename)
            f.write(arg + " ")
        f.write("\nExecution done.\n")

if __name__ == "__main__":
    main()
