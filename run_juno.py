
"""
Simple script to run Juno programs with minimal output.
This script directly executes Juno programs without showing any interpreter messages.
"""

import os
import sys
import subprocess

def main():
    """Main entry point."""
    # Get the file to run
    if len(sys.argv) < 2:
        print("Usage: python run_juno.py <juno_file>")
        return 1
    
    file_path = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return 1
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Run the Juno interpreter
    juno_standalone = os.path.join(script_dir, "juno_standalone.py")
    
    # Run the file with the standalone interpreter - completely silent mode
    with open(os.devnull, 'w') as devnull:
        # Capture and filter the output
        process = subprocess.Popen(
            [sys.executable, juno_standalone, file_path],
            stdout=subprocess.PIPE,
            stderr=devnull,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        # Process the output line by line
        for line in process.stdout:
            # Skip lines that contain interpreter messages
            if "Using direct interpreter" not in line and \
               "Executing Juno file" not in line and \
               "=" * 10 not in line and \
               "Execution completed" not in line:
                # Print the actual program output
                print(line.rstrip())

        # Wait for the process to complete
        result = process.wait()
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())