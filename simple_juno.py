#!/usr/bin/env python3
"""
Simple Juno Interpreter - Minimal version that only shows program output
"""

import os
import sys
import re
import importlib.util

# Import the package system
from simple_juno_import import import_package

# Import GUI library if available
try:
    import fixed_juno_gui as juno_gui
    HAS_GUI = True
except ImportError:
    try:
        import juno_gui
        HAS_GUI = True
    except ImportError:
        HAS_GUI = False

def execute_juno(file_path):
    """Execute a Juno file and show only the program output."""
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()

        # Process the file line by line
        lines = source.split('\n')
        i = 0
        local_vars = {}
        imported_packages = {}

        # Add GUI functions if available
        if HAS_GUI:
            # Add GUI functions to local variables
            local_vars["GUI"] = juno_gui
        
        while i < len(lines):
            line = lines[i].strip()
            i += 1
            
            # Skip empty lines and comments
            if not line or line.startswith('//'):
                continue

            # Handle imports
            if line.startswith("import "):
                import_stmt = line.strip()
                if import_stmt.endswith(';'):
                    import_stmt = import_stmt[:-1]

                # Extract package and class
                import_parts = import_stmt[7:].strip().split('.')
                if len(import_parts) >= 2:
                    package_name = import_parts[0]
                    class_name = import_parts[1]

                    # Import the package if not already imported
                    if package_name not in imported_packages:
                        imported_packages[package_name] = import_package(package_name)

                    # Add the class to local variables
                    if package_name in imported_packages:
                        if class_name in imported_packages[package_name]:
                            local_vars[class_name] = imported_packages[package_name][class_name]
                        elif "juno_" + package_name in imported_packages[package_name]:
                            local_vars[class_name] = imported_packages[package_name]["juno_" + package_name]
            
            # Handle GUI method calls
            if HAS_GUI and "GUI." in line:
                # Extract method call
                gui_call = line.strip()
                if gui_call.endswith(';'):
                    gui_call = gui_call[:-1]

                # Extract method name and arguments
                if '=' in gui_call:
                    # Assignment to a variable
                    var_name, method_call = gui_call.split('=', 1)
                    var_name = var_name.strip()
                    method_call = method_call.strip()

                    if method_call.startswith("GUI."):
                        method_name = method_call.split('(')[0].replace("GUI.", "")
                        args_str = method_call[method_call.find('(')+1:method_call.rfind(')')]

                        # Process arguments
                        args = []
                        if args_str:
                            for arg in args_str.split(','):
                                arg = arg.strip()
                                if arg.startswith('"') and arg.endswith('"'):
                                    args.append(arg[1:-1])
                                elif arg.startswith("'") and arg.endswith("'"):
                                    args.append(arg[1:-1])
                                elif arg in local_vars:
                                    args.append(local_vars[arg])
                                elif arg.isdigit():
                                    args.append(int(arg))
                                else:
                                    args.append(arg)

                        # Call the method
                        if hasattr(juno_gui, method_name):
                            result = getattr(juno_gui, method_name)(*args)
                            local_vars[var_name] = result
                else:
                    # Direct method call
                    if gui_call.startswith("GUI."):
                        method_name = gui_call.split('(')[0].replace("GUI.", "")
                        args_str = gui_call[gui_call.find('(')+1:gui_call.rfind(')')]

                        # Process arguments
                        args = []
                        if args_str:
                            for arg in args_str.split(','):
                                arg = arg.strip()
                                if arg.startswith('"') and arg.endswith('"'):
                                    args.append(arg[1:-1])
                                elif arg.startswith("'") and arg.endswith("'"):
                                    args.append(arg[1:-1])
                                elif arg in local_vars:
                                    args.append(local_vars[arg])
                                elif arg.isdigit():
                                    args.append(int(arg))
                                else:
                                    args.append(arg)

                        # Call the method
                        if hasattr(juno_gui, method_name):
                            getattr(juno_gui, method_name)(*args)

            # Handle System.out.println statements
            elif "System.out.println" in line:
                # Extract content inside println()
                content_start = line.find("System.out.println(") + len("System.out.println(")
                content_end = line.rfind(")")
                content = line[content_start:content_end].strip()
                
                # Remove semicolon if present
                if content.endswith(";"):
                    content = content[:-1]
                
                # Handle string literals
                if content.startswith('"') and content.endswith('"'):
                    print(content[1:-1], flush=True)
                elif content.startswith("'") and content.endswith("'"):
                    print(content[1:-1], flush=True)
                # Handle variables
                elif content in local_vars:
                    print(local_vars[content], flush=True)
                # Handle expressions with variables and concatenation
                elif '+' in content:
                    # Process each part of the expression
                    parts = []
                    current_part = ""
                    in_string = False
                    string_delimiter = None
                    
                    for char in content:
                        if char in ['"', "'"]:
                            if not in_string:
                                in_string = True
                                string_delimiter = char
                            elif char == string_delimiter:
                                in_string = False
                                string_delimiter = None
                            current_part += char
                        elif char == '+' and not in_string:
                            parts.append(current_part.strip())
                            current_part = ""
                        else:
                            current_part += char
                    
                    # Add the last part
                    if current_part:
                        parts.append(current_part.strip())
                    
                    # Evaluate each part
                    result = ""
                    for part in parts:
                        if part.startswith('"') and part.endswith('"'):
                            result += part[1:-1]
                        elif part.startswith("'") and part.endswith("'"):
                            result += part[1:-1]
                        elif part in local_vars:
                            result += str(local_vars[part])
                        elif part.startswith('(') and part.endswith(')'):
                            # Handle expressions in parentheses
                            expr = part[1:-1].strip()
                            if expr in local_vars:
                                result += str(local_vars[expr])
                            elif '+' in expr and expr.replace('+', '').strip().isdigit():
                                # Simple addition
                                try:
                                    result += str(eval(expr))
                                except:
                                    result += expr
                            else:
                                result += expr
                        else:
                            result += part
                    
                    print(result, flush=True)
                else:
                    # For other expressions, just print the raw content
                    print(f"{content}", flush=True)
            
            # Handle variable declarations with Java-style types
            elif any(type_name in line for type_name in ["String", "int", "double", "boolean", "float", "long"]) and "=" in line:
                var_decl = line.strip()
                if '=' in var_decl:
                    var_name_part, var_value = var_decl.split('=', 1)
                    var_name = var_name_part.split()[-1].strip()  # Get the last part (variable name)
                    var_value = var_value.strip()
                    
                    # Remove semicolon if present
                    if var_value.endswith(';'):
                        var_value = var_value[:-1]
                    
                    # Handle string literals
                    if var_value.startswith('"') and var_value.endswith('"'):
                        local_vars[var_name] = var_value[1:-1]
                    elif var_value.startswith("'") and var_value.endswith("'"):
                        local_vars[var_name] = var_value[1:-1]
                    # Handle numbers
                    elif var_value.isdigit():
                        local_vars[var_name] = int(var_value)
                    elif var_value.replace('.', '', 1).isdigit():
                        local_vars[var_name] = float(var_value)
                    else:
                        local_vars[var_name] = var_value
        
        return 0
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python simple_juno.py <juno_file>")
        return 1
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return 1
    
    return execute_juno(file_path)

if __name__ == "__main__":
    sys.exit(main())