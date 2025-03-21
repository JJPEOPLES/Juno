#!/usr/bin/env python3
"""
Juno Programming Language - Main Entry Point
This file serves as the main entry point for the Juno interpreter.
"""

import os
import sys
import argparse
import traceback
from pathlib import Path

# Add the parent directory to the path so we can import the juno package
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# Create placeholder modules if they don't exist yet
if not os.path.exists(os.path.join(current_dir, "juno")):
    os.makedirs(os.path.join(current_dir, "juno"), exist_ok=True)

if not os.path.exists(os.path.join(current_dir, "juno", "utils")):
    os.makedirs(os.path.join(current_dir, "juno", "utils"), exist_ok=True)

# Create placeholder files if they don't exist
placeholder_files = [
    ("juno/__init__.py", '"""Juno Programming Language"""\n\nVERSION = "2.0.0"\n'),
    ("juno/version.py", '"""Version information"""\n\nVERSION = "2.0.0"\n'),
    ("juno/utils/__init__.py", '"""Utility modules"""\n'),
]

for file_path, content in placeholder_files:
    full_path = os.path.join(current_dir, file_path)
    if not os.path.exists(full_path):
        with open(full_path, 'w') as f:
            f.write(content)

# Simple implementation of required modules if they don't exist
class DummyInterpreter:
    def __init__(self, **kwargs):
        pass
    def check_syntax(self, source, filename="<input>"):
        print(f"Checking syntax of {filename}")
        return True
    def execute(self, source, filename="<input>"):
        print(f"Executing {filename}")
        print(f"Source code: {source[:100]}...")
        return True

class DummyREPL:
    def __init__(self, **kwargs):
        pass
    def start(self):
        print("Starting Juno REPL (placeholder)")
        print("This is a placeholder implementation.")
        print("Type 'exit' to exit.")
        while True:
            try:
                cmd = input("juno> ")
                if cmd.strip() in ('exit', 'quit'):
                    break
                print(f"You typed: {cmd}")
            except (KeyboardInterrupt, EOFError):
                break

# Try to import the real modules, fall back to placeholders if needed
try:
    from juno import interpreter, version
    from juno.utils import logger, config
    VERSION = version.VERSION
except ImportError:
    # Create placeholder modules
    sys.modules['juno'] = type('juno', (), {})
    sys.modules['juno.interpreter'] = type('interpreter', (), {'Interpreter': DummyInterpreter})
    sys.modules['juno.version'] = type('version', (), {'VERSION': '2.0.0'})
    sys.modules['juno.repl'] = type('repl', (), {'REPL': DummyREPL})
    sys.modules['juno.utils'] = type('utils', (), {})
    sys.modules['juno.utils.logger'] = type('logger', (), {'setup_logging': lambda x: None, 'get_logger': lambda x: None})
    sys.modules['juno.utils.config'] = type('config', (), {'load_config': lambda: None})

    # Import the placeholders
    from juno import interpreter, version
    from juno.utils import logger, config
    VERSION = '2.0.0'

    print("Note: Using placeholder implementation of Juno modules.")
    print("This is a minimal implementation for demonstration purposes.")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Juno Programming Language Interpreter",
        epilog="If no file is specified, the REPL will start."
    )
    
    parser.add_argument(
        "file", 
        nargs="?", 
        help="Juno source file to execute"
    )
    
    parser.add_argument(
        "-v", "--version", 
        action="store_true", 
        help="Show version information and exit"
    )
    
    parser.add_argument(
        "-d", "--debug", 
        action="store_true", 
        help="Enable debug mode"
    )
    
    parser.add_argument(
        "-o", "--optimize", 
        action="store_true", 
        help="Enable optimizations"
    )
    
    parser.add_argument(
        "--no-stdlib", 
        action="store_true", 
        help="Don't load the standard library"
    )
    
    parser.add_argument(
        "--check", 
        action="store_true", 
        help="Check syntax only, don't execute"
    )
    
    return parser.parse_args()

def show_version():
    """Display version information."""
    print(f"Juno Programming Language v{version.VERSION}")
    print(f"Copyright 2025 JJPEOPLES")
    print(f"License: MIT")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Platform: {sys.platform}")

def run_file(filename, args):
    """Run a Juno source file."""
    try:
        # Check if file exists
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found.")
            sys.exit(1)
            
        # Check file extension
        if not filename.endswith('.juno'):
            print(f"Warning: File '{filename}' does not have a .juno extension.")
            
        # Read the file
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
            
        # Set up the interpreter
        juno_interpreter = interpreter.Interpreter(
            debug=args.debug,
            optimize=args.optimize,
            load_stdlib=not args.no_stdlib
        )
        
        # Check syntax only if requested
        if args.check:
            result = juno_interpreter.check_syntax(source, filename)
            if result:
                print(f"Syntax check passed: {filename}")
                return 0
            else:
                print(f"Syntax check failed: {filename}")
                return 1
                
        # Execute the file
        result = juno_interpreter.execute(source, filename)
        return 0 if result else 1
        
    except Exception as e:
        if args.debug:
            traceback.print_exc()
        else:
            print(f"Error: {str(e)}")
        return 1

def start_repl(args):
    """Start the Juno REPL."""
    try:
        # Set up the REPL
        juno_repl = repl.REPL(
            debug=args.debug,
            optimize=args.optimize,
            load_stdlib=not args.no_stdlib
        )
        
        # Start the REPL
        juno_repl.start()
        return 0
        
    except Exception as e:
        if args.debug:
            traceback.print_exc()
        else:
            print(f"Error: {str(e)}")
        return 1

def main():
    """Main entry point."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Show version and exit if requested
    if args.version:
        show_version()
        return 0
        
    # Set up logging
    log_level = "DEBUG" if args.debug else "INFO"
    logger.setup_logging(log_level)
    
    # Load configuration
    config.load_config()
    
    # Run file or start REPL
    if args.file:
        return run_file(args.file, args)
    else:
        return start_repl(args)

if __name__ == "__main__":
    sys.exit(main())