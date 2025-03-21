#!/usr/bin/env python3
"""
Direct Juno executor - runs Juno programs with no interpreter messages.
This script directly executes Juno programs and only shows the program output.
"""

import os
import sys
import traceback

# Import the standalone interpreter
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from juno_standalone import Interpreter

def main():
    """Main entry point."""
    # Get the file to run
    if len(sys.argv) < 2:
        print("Usage: python juno_direct.py <juno_file>")
        return 1
    
    file_path = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return 1
    
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Create an interpreter with quiet mode
        interpreter = Interpreter(quiet=True)
        
        # Execute the file
        result = interpreter.execute(source, file_path)
        return 0 if result else 1
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())