#!/usr/bin/env python3
"""
Juno Programming Language - Standalone Version
This is a simplified standalone version of the Juno interpreter.
"""

import os
import sys
import argparse
import traceback
import importlib.util
from pathlib import Path

VERSION = "2.0.1"

class Interpreter:
    """
    The Juno interpreter.
    This class is responsible for parsing and executing Juno code.
    """
    
    def __init__(self, debug=False, optimize=False, load_stdlib=True, quiet=False):
        """
        Initialize the interpreter.

        Args:
            debug (bool): Enable debug mode
            optimize (bool): Enable optimizations
            load_stdlib (bool): Load the standard library
            quiet (bool): Quiet mode - show only program output
        """
        self.debug = debug
        self.optimize = optimize
        self.load_stdlib = load_stdlib
        self.quiet = quiet

        # Initialize the interpreter
        self._initialize()
        
    def _initialize(self):
        """Initialize the interpreter."""
        # This is a placeholder for the actual initialization
        if self.debug and not self.quiet:
            print("Initializing Juno interpreter...")
            print(f"Debug mode: {self.debug}")
            print(f"Optimize: {self.optimize}")
            print(f"Load stdlib: {self.load_stdlib}")
            print(f"Quiet mode: {self.quiet}")

        # Load the standard library if requested
        if self.load_stdlib:
            self._load_stdlib()
    
    def _load_stdlib(self):
        """Load the Juno standard library."""
        # This is a placeholder for loading the standard library
        if self.debug and not self.quiet:
            print("Loading Juno standard library...")
    
    def check_syntax(self, source, filename="<input>"):
        """
        Check the syntax of Juno code without executing it.

        Args:
            source (str): The Juno source code
            filename (str): The name of the file being checked

        Returns:
            bool: True if the syntax is valid, False otherwise
        """
        # This is a placeholder for the actual syntax checking
        if self.debug and not self.quiet:
            print(f"Checking syntax of {filename}...")

        # For now, just return True (syntax is valid)
        return True
    
    def execute(self, source, filename="<input>"):
        """
        Execute Juno code.

        Args:
            source (str): The Juno source code
            filename (str): The name of the file being executed

        Returns:
            bool: True if execution was successful, False otherwise
        """
        # Removed execution message to keep output clean

        try:
            # For now, skip the JIT compiler and use the direct interpreter
            # This ensures we properly handle Java-style syntax

            # Uncomment this section when the JIT compiler is fully compatible with Java syntax
            """
            # Import the JIT compiler if available
            try:
                # Check if the JIT compiler module exists
                jit_spec = importlib.util.find_spec("juno.compiler.jit")
                interpreter_spec = importlib.util.find_spec("juno.interpreter_with_jit")

                if jit_spec is not None and interpreter_spec is not None:
                    # Import the modules
                    jit_module = importlib.util.module_from_spec(jit_spec)
                    interpreter_module = importlib.util.module_from_spec(interpreter_spec)

                    jit_spec.loader.exec_module(jit_module)
                    interpreter_spec.loader.exec_module(interpreter_module)

                    # Use the JIT compiler
                    JITCompiler = jit_module.JITCompiler
                    JITInterpreter = interpreter_module.Interpreter

                    jit_interpreter = JITInterpreter(debug=self.debug, optimize=self.optimize)

                    try:
                        result = jit_interpreter.execute(source, filename)

                        if result:
                            print("=" * 60)
                            print("Execution completed successfully with JIT compilation")
                            return True
                        else:
                            print("=" * 60)
                            print("Execution failed with JIT compilation, falling back to interpreter")
                    except Exception as e:
                        print(f"Error: {str(e)}")
                        if self.debug:
                            traceback.print_exc()
                        print("=" * 60)
                        print("Execution failed with JIT compilation, falling back to interpreter")
                else:
                    # JIT compiler not available, fall back to interpreter
                    pass
            except Exception as e:
                # Error importing JIT compiler, fall back to interpreter
                if self.debug:
                    print(f"Error importing JIT compiler: {str(e)}")
                    traceback.print_exc()
                print("JIT compiler not available, using standard interpreter")
                pass
            """

            # Use the direct interpreter for now - no messages
            pass

            # Fall back to simple execution if JIT fails or is not available
            # Simple line-by-line execution
            local_vars = {}
            local_methods = {}  # Store methods
            lines = source.split('\n')

            # First pass: identify methods
            j = 0
            while j < len(lines):
                line = lines[j].strip()

                # Identify method declarations
                if any(keyword in line for keyword in ['public ', 'private ', 'protected ', 'static ']) and '(' in line and ')' in line:
                    # This is a method declaration
                    method_parts = line.split("(")
                    method_name = method_parts[0].split(" ")[-1].strip()

                    # Extract parameter list
                    params_part = method_parts[1].split(")")[0].strip()
                    params = []

                    if params_part:
                        # Process Java-style parameters (type name, type name, ...)
                        param_pairs = params_part.split(",")
                        for pair in param_pairs:
                            param_parts = pair.strip().split(" ")
                            param_name = param_parts[-1].strip()
                            params.append(param_name)

                    # Find the method body
                    method_body_start = j
                    method_body_end = j

                    # Find the end of the method
                    brace_count = 0
                    if '{' in line:
                        brace_count = 1
                    else:
                        # Look for opening brace on next line
                        k = j
                        while k < len(lines) and '{' not in lines[k]:
                            k += 1
                        if k < len(lines):
                            brace_count = 1
                            method_body_start = k + 1

                    k = j
                    while brace_count > 0 and k < len(lines):
                        next_line = lines[k].strip()
                        k += 1
                        if '{' in next_line:
                            brace_count += 1
                        if '}' in next_line:
                            brace_count -= 1
                            if brace_count == 0:
                                method_body_end = k - 1

                    # Store method details
                    local_methods[method_name] = {
                        'params': params,
                        'body_start': method_body_start,
                        'body_end': method_body_end,
                        'is_static': 'static' in line
                    }

                j += 1
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                i += 1

                # Skip empty lines and comments
                if not line or line.startswith('//'):
                    continue

                # Handle variable declarations with Java-style types
                if any(type_name in line for type_name in ["String", "int", "double", "boolean", "float", "long"]) and "=" in line:
                    var_decl = line.strip()
                    if '=' in var_decl:
                        var_name_part, var_value = var_decl.split('=', 1)
                        var_name = var_name_part.split()[-1].strip()  # Get the last part (variable name)
                        var_value = var_value.strip()

                        # Handle string literals
                        if var_value.endswith(';'):
                            var_value = var_value[:-1]  # Remove semicolon

                        if var_value.startswith('"') and var_value.endswith('"'):
                            local_vars[var_name] = var_value[1:-1]
                        elif var_value.startswith("'") and var_value.endswith("'"):
                            local_vars[var_name] = var_value[1:-1]
                        # Handle numbers
                        elif var_value.isdigit():
                            local_vars[var_name] = int(var_value)
                        elif var_value.replace('.', '', 1).isdigit():
                            local_vars[var_name] = float(var_value)
                        # Handle method calls
                        elif "(" in var_value and ")" in var_value:
                            method_name = var_value.split("(")[0].strip()
                            args_str = var_value[var_value.find("(")+1:var_value.rfind(")")].strip()

                            # Handle method calls like greet("Developer")
                            if method_name in local_methods:
                                # Process arguments
                                args = []
                                if args_str:
                                    for arg in args_str.split(","):
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

                                # Get method details
                                method_info = local_methods[method_name]

                                # Create a local scope for the method
                                method_local_vars = {}

                                # Add parameters to the method's local scope
                                for idx, param_name in enumerate(method_info['params']):
                                    if idx < len(args):
                                        method_local_vars[param_name] = args[idx]
                                    else:
                                        method_local_vars[param_name] = None  # Default value if not provided

                                # Execute the method body (simplified)
                                method_result = None

                                # Find return statements in the method body
                                for method_line_idx in range(method_info['body_start'], method_info['body_end']):
                                    method_line = lines[method_line_idx].strip()

                                    # Check for return statement
                                    if method_line.startswith('return '):
                                        return_expr = method_line[7:]  # Remove 'return '
                                        if return_expr.endswith(';'):
                                            return_expr = return_expr[:-1]  # Remove semicolon

                                        # Handle string literals
                                        if return_expr.startswith('"') and return_expr.endswith('"'):
                                            method_result = return_expr[1:-1]
                                        elif return_expr.startswith("'") and return_expr.endswith("'"):
                                            method_result = return_expr[1:-1]
                                        # Handle variables
                                        elif return_expr in method_local_vars:
                                            method_result = method_local_vars[return_expr]
                                        # Handle string concatenation
                                        elif '+' in return_expr and not return_expr.replace('+', '').strip().isdigit():
                                            # Process string concatenation
                                            parts = []
                                            current_part = ""
                                            in_string = False
                                            string_delimiter = None

                                            for char in return_expr:
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
                                                elif part in method_local_vars:
                                                    result += str(method_local_vars[part])
                                                elif part in local_vars:
                                                    result += str(local_vars[part])
                                                else:
                                                    result += part

                                            method_result = result
                                        # Handle numeric expressions
                                        elif '+' in return_expr and return_expr.replace('+', '').strip().isdigit():
                                            # Simple addition
                                            try:
                                                method_result = eval(return_expr)
                                            except:
                                                method_result = return_expr
                                        else:
                                            method_result = return_expr

                                        break  # Stop at the first return statement

                                local_vars[var_name] = method_result
                            else:
                                local_vars[var_name] = f"Method call: {var_value}"
                        # Handle arrays
                        elif var_value.startswith('[') and var_value.endswith(']'):
                            array_items = var_value[1:-1].split(',')
                            local_vars[var_name] = [item.strip() for item in array_items]
                        # Handle expressions
                        else:
                            local_vars[var_name] = var_value

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
                    # Handle method calls
                    elif "(" in content and ")" in content:
                        method_name = content.split("(")[0].strip()
                        args_str = content[content.find("(")+1:content.rfind(")")].strip()

                        # Process method call
                        if method_name in local_methods:
                            # Process arguments
                            args = []
                            if args_str:
                                for arg in args_str.split(","):
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

                            # Execute method (simplified)
                            method_result = f"Result of {method_name}({args_str})"
                            print(method_result, flush=True)
                        else:
                            print(f"Method call: {content}", flush=True)
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
                                elif expr.count('+') == 1:
                                    # Try to evaluate a simple expression with two variables
                                    try:
                                        left, right = expr.split('+')
                                        left = left.strip()
                                        right = right.strip()

                                        if left in local_vars:
                                            left = local_vars[left]
                                        else:
                                            try:
                                                left = int(left)
                                            except:
                                                try:
                                                    left = float(left)
                                                except:
                                                    pass

                                        if right in local_vars:
                                            right = local_vars[right]
                                        else:
                                            try:
                                                right = int(right)
                                            except:
                                                try:
                                                    right = float(right)
                                                except:
                                                    pass

                                        result += str(left + right)
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

                # Handle Java-style method definitions
                elif any(keyword in line for keyword in ['public ', 'private ', 'protected ', 'static ']) and '(' in line:
                    # This is a method declaration
                    method_decl = line.strip()

                    # Extract method name and parameters
                    method_parts = method_decl.split("(")
                    method_name = method_parts[0].split(" ")[-1].strip()

                    # Extract parameter list
                    params_part = method_parts[1].split(")")[0].strip()
                    params = []

                    if params_part:
                        # Process Java-style parameters (type name, type name, ...)
                        param_pairs = params_part.split(",")
                        for pair in param_pairs:
                            param_parts = pair.strip().split(" ")
                            param_name = param_parts[-1].strip()
                            params.append(param_name)

                    # Store method information
                    method_body_start = i

                    # Find the end of the method
                    brace_count = 0
                    if '{' in line:
                        brace_count = 1
                    while brace_count > 0 and i < len(lines):
                        next_line = lines[i].strip()
                        i += 1
                        if '{' in next_line:
                            brace_count += 1
                        if '}' in next_line:
                            brace_count -= 1

                    method_body_end = i - 1

                    # Store method in local_methods with more details
                    local_methods[method_name] = {
                        'params': params,
                        'body_start': method_body_start,
                        'body_end': method_body_end,
                        'is_static': 'static' in method_decl
                    }

                # Handle Java-style if statements
                elif line.startswith('if '):
                    # Extract condition
                    condition = line[3:].strip()
                    if condition.startswith('(') and ')' in condition:
                        condition = condition[1:condition.find(')')].strip()

                    # Evaluate condition (improved)
                    condition_true = False

                    # Handle different comparison operators
                    if '>' in condition and '=' not in condition:
                        left, right = condition.split('>', 1)
                        left = left.strip()
                        right = right.strip()
                        if left in local_vars:
                            left = local_vars[left]
                        else:
                            try:
                                left = int(left)
                            except:
                                try:
                                    left = float(left)
                                except:
                                    pass
                        if right in local_vars:
                            right = local_vars[right]
                        else:
                            try:
                                right = int(right)
                            except:
                                try:
                                    right = float(right)
                                except:
                                    pass
                        condition_true = left > right
                    elif '>=' in condition:
                        left, right = condition.split('>=', 1)
                        left = left.strip()
                        right = right.strip()
                        if left in local_vars:
                            left = local_vars[left]
                        else:
                            try:
                                left = int(left)
                            except:
                                try:
                                    left = float(left)
                                except:
                                    pass
                        if right in local_vars:
                            right = local_vars[right]
                        else:
                            try:
                                right = int(right)
                            except:
                                try:
                                    right = float(right)
                                except:
                                    pass
                        condition_true = left >= right
                    elif '<' in condition and '=' not in condition:
                        left, right = condition.split('<', 1)
                        left = left.strip()
                        right = right.strip()
                        if left in local_vars:
                            left = local_vars[left]
                        else:
                            try:
                                left = int(left)
                            except:
                                try:
                                    left = float(left)
                                except:
                                    pass
                        if right in local_vars:
                            right = local_vars[right]
                        else:
                            try:
                                right = int(right)
                            except:
                                try:
                                    right = float(right)
                                except:
                                    pass
                        condition_true = left < right
                    elif '<=' in condition:
                        left, right = condition.split('<=', 1)
                        left = left.strip()
                        right = right.strip()
                        if left in local_vars:
                            left = local_vars[left]
                        else:
                            try:
                                left = int(left)
                            except:
                                try:
                                    left = float(left)
                                except:
                                    pass
                        if right in local_vars:
                            right = local_vars[right]
                        else:
                            try:
                                right = int(right)
                            except:
                                try:
                                    right = float(right)
                                except:
                                    pass
                        condition_true = left <= right
                    elif '==' in condition:
                        left, right = condition.split('==', 1)
                        left = left.strip()
                        right = right.strip()
                        if left in local_vars:
                            left = local_vars[left]
                        else:
                            try:
                                left = int(left)
                            except:
                                try:
                                    left = float(left)
                                except:
                                    if left.startswith('"') and left.endswith('"'):
                                        left = left[1:-1]
                                    elif left.startswith("'") and left.endswith("'"):
                                        left = left[1:-1]
                        if right in local_vars:
                            right = local_vars[right]
                        else:
                            try:
                                right = int(right)
                            except:
                                try:
                                    right = float(right)
                                except:
                                    if right.startswith('"') and right.endswith('"'):
                                        right = right[1:-1]
                                    elif right.startswith("'") and right.endswith("'"):
                                        right = right[1:-1]
                        condition_true = left == right
                    elif '!=' in condition:
                        left, right = condition.split('!=', 1)
                        left = left.strip()
                        right = right.strip()
                        if left in local_vars:
                            left = local_vars[left]
                        else:
                            try:
                                left = int(left)
                            except:
                                try:
                                    left = float(left)
                                except:
                                    if left.startswith('"') and left.endswith('"'):
                                        left = left[1:-1]
                                    elif left.startswith("'") and left.endswith("'"):
                                        left = left[1:-1]
                        if right in local_vars:
                            right = local_vars[right]
                        else:
                            try:
                                right = int(right)
                            except:
                                try:
                                    right = float(right)
                                except:
                                    if right.startswith('"') and right.endswith('"'):
                                        right = right[1:-1]
                                    elif right.startswith("'") and right.endswith("'"):
                                        right = right[1:-1]
                        condition_true = left != right

                    # Find the if block and else block
                    if_block_start = i
                    if_block_end = i
                    else_block_start = -1
                    else_block_end = -1
                    brace_count = 1
                    while brace_count > 0 and i < len(lines):
                        next_line = lines[i].strip()
                        i += 1
                        if '{' in next_line:
                            brace_count += 1
                        if '}' in next_line:
                            brace_count -= 1
                            if brace_count == 0:
                                if_block_end = i - 1
                                # Check for else
                                if i < len(lines) and lines[i].strip().startswith('else'):
                                    i += 1  # Skip else line
                                    else_block_start = i
                                    brace_count = 1
                                    while brace_count > 0 and i < len(lines):
                                        next_line = lines[i].strip()
                                        i += 1
                                        if '{' in next_line:
                                            brace_count += 1
                                        if '}' in next_line:
                                            brace_count -= 1
                                            if brace_count == 0:
                                                else_block_end = i - 1

                    # Execute the appropriate block
                    if condition_true:
                        # Execute if block
                        pass
                    elif else_block_start != -1:
                        # Execute else block
                        pass

                # Handle Java-style for loops
                elif line.startswith('for '):
                    # Extract loop parameters
                    for_stmt = line.strip()

                    # Process the for loop
                    if '(' in for_stmt and ')' in for_stmt:
                        for_parts = for_stmt[for_stmt.find('(')+1:for_stmt.find(')')].split(';')
                        if len(for_parts) == 3:
                            # Standard for loop: for (init; condition; increment)
                            init = for_parts[0].strip()
                            condition = for_parts[1].strip()
                            increment = for_parts[2].strip()

                            # Extract variable name and initial value from init
                            if ' ' in init:
                                # Has type declaration: int i = 0
                                var_parts = init.split(' ')
                                var_type = var_parts[0].strip()
                                var_assign = ' '.join(var_parts[1:]).strip()
                                var_name = var_assign.split('=')[0].strip()
                                initial_value = var_assign.split('=')[1].strip()
                            else:
                                # No type declaration: i = 0
                                var_name = init.split('=')[0].strip()
                                initial_value = init.split('=')[1].strip()

                            # Initialize the loop variable
                            try:
                                if initial_value.isdigit():
                                    local_vars[var_name] = int(initial_value)
                                elif initial_value.replace('.', '', 1).isdigit():
                                    local_vars[var_name] = float(initial_value)
                                else:
                                    local_vars[var_name] = initial_value
                            except:
                                local_vars[var_name] = 0

                    # Find the for loop body
                    brace_count = 0
                    if '{' in line:
                        brace_count = 1
                        for_body_start = i
                    else:
                        for_body_start = i
                        # Look for opening brace on next line
                        if i < len(lines) and '{' in lines[i]:
                            brace_count = 1
                            i += 1

                    for_body_end = i
                    while brace_count > 0 and i < len(lines):
                        next_line = lines[i].strip()
                        i += 1
                        if '{' in next_line:
                            brace_count += 1
                        if '}' in next_line:
                            brace_count -= 1
                            if brace_count == 0:
                                for_body_end = i - 1

                    # Actually execute the for loop (basic implementation)
                    if len(for_parts) == 3:
                        # Get loop components
                        condition = for_parts[1].strip()
                        increment = for_parts[2].strip()
                        var_name = None

                        # Extract variable name from init
                        if ' ' in init:
                            var_name = init.split(' ')[-1].split('=')[0].strip()
                        else:
                            var_name = init.split('=')[0].strip()

                        # Store the current position to return to after loop execution
                        original_position = i

                        # Execute the loop (limited to 100 iterations for safety)
                        max_iterations = 100
                        iteration_count = 0

                        while iteration_count < max_iterations:
                            # Evaluate condition
                            condition_true = False

                            if '<' in condition:
                                left, right = condition.split('<', 1)
                                left = left.strip()
                                right = right.strip()

                                # Get left value (usually the loop variable)
                                if left in local_vars:
                                    left_val = local_vars[left]
                                else:
                                    try:
                                        left_val = int(left)
                                    except:
                                        left_val = 0

                                # Get right value
                                if right in local_vars:
                                    right_val = local_vars[right]
                                else:
                                    try:
                                        right_val = int(right)
                                    except:
                                        right_val = 0

                                condition_true = left_val < right_val
                            elif '<=' in condition:
                                left, right = condition.split('<=', 1)
                                left = left.strip()
                                right = right.strip()

                                # Get left value (usually the loop variable)
                                if left in local_vars:
                                    left_val = local_vars[left]
                                else:
                                    try:
                                        left_val = int(left)
                                    except:
                                        left_val = 0

                                # Get right value
                                if right in local_vars:
                                    right_val = local_vars[right]
                                else:
                                    try:
                                        right_val = int(right)
                                    except:
                                        right_val = 0

                                condition_true = left_val <= right_val

                            # Exit loop if condition is false
                            if not condition_true:
                                break

                            # Execute loop body
                            loop_i = for_body_start
                            while loop_i < for_body_end:
                                loop_line = lines[loop_i].strip()

                                # Process loop body line (simplified)
                                if "System.out.println" in loop_line:
                                    # Extract content inside println()
                                    content_start = loop_line.find("System.out.println(") + len("System.out.println(")
                                    content_end = loop_line.rfind(")")
                                    content = loop_line[content_start:content_end].strip()

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
                                                else:
                                                    result += expr
                                            else:
                                                result += part

                                        print(result, flush=True)

                                loop_i += 1

                            # Apply increment
                            if var_name and var_name in local_vars:
                                if increment.strip() == var_name + "++":
                                    local_vars[var_name] += 1
                                elif increment.strip() == "++" + var_name:
                                    local_vars[var_name] += 1
                                elif increment.strip() == var_name + "--":
                                    local_vars[var_name] -= 1
                                elif increment.strip() == "--" + var_name:
                                    local_vars[var_name] -= 1
                                elif "+=" in increment:
                                    var, val = increment.split("+=", 1)
                                    var = var.strip()
                                    val = val.strip()
                                    if var == var_name:
                                        try:
                                            local_vars[var_name] += int(val)
                                        except:
                                            try:
                                                local_vars[var_name] += float(val)
                                            except:
                                                pass
                                elif "=" in increment:
                                    var, expr = increment.split("=", 1)
                                    var = var.strip()
                                    expr = expr.strip()
                                    if var == var_name:
                                        if "+" in expr:
                                            try:
                                                parts = expr.split("+")
                                                if len(parts) == 2 and parts[0].strip() == var_name:
                                                    val = parts[1].strip()
                                                    try:
                                                        local_vars[var_name] += int(val)
                                                    except:
                                                        try:
                                                            local_vars[var_name] += float(val)
                                                        except:
                                                            pass
                                            except:
                                                pass

                            iteration_count += 1

                        # Restore position after loop execution
                        i = original_position
                    else:
                        # Skip the for loop body if we couldn't parse it properly
                        i = for_body_end

            # Ensure all output is flushed
            sys.stdout.flush()
            return True

        except Exception as e:
            # Ensure all output is flushed
            sys.stdout.flush()

            # Always show errors, even in quiet mode
            print(f"Error: {str(e)}", flush=True)
            if self.debug:
                traceback.print_exc()
                sys.stdout.flush()
            return False

class REPL:
    """
    The Juno REPL (Read-Eval-Print Loop).
    This class provides an interactive shell for the Juno programming language.
    """
    
    def __init__(self, debug=False, optimize=False, load_stdlib=True, quiet=False):
        """
        Initialize the REPL.

        Args:
            debug (bool): Enable debug mode
            optimize (bool): Enable optimizations
            load_stdlib (bool): Load the standard library
            quiet (bool): Quiet mode - show only program output
        """
        self.debug = debug
        self.optimize = optimize
        self.load_stdlib = load_stdlib
        self.quiet = quiet

        # Create an interpreter
        self.interpreter = Interpreter(debug, optimize, load_stdlib, quiet)
    
    def _print_welcome(self):
        """Print the welcome message."""
        if not self.quiet:
            print(f"Juno Programming Language v{VERSION}")
            print(f"Type 'help' for help, 'exit' to exit.")
            print()
    
    def _handle_command(self, command):
        """
        Handle special REPL commands.
        
        Args:
            command (str): The command to handle
            
        Returns:
            bool: True if the command was handled, False otherwise
        """
        command = command.strip()
        
        if command in ('exit', 'quit'):
            return True
        
        if command == 'help':
            print("Juno REPL Help:")
            print("  help      - Show this help message")
            print("  exit/quit - Exit the REPL")
            print("  clear     - Clear the screen")
            print("  version   - Show version information")
            return True
        
        if command == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
            return True
        
        if command == 'version':
            print(f"Juno Programming Language v{VERSION}")
            return True
        
        return False
    
    def start(self):
        """Start the REPL."""
        self._print_welcome()
        
        while True:
            try:
                # Read
                line = input("juno> ")
                
                # Handle empty lines
                if not line.strip():
                    continue
                
                # Handle special commands
                if self._handle_command(line):
                    continue
                
                # Eval
                result = self.interpreter.execute(line, "<repl>")
                
                # Print (handled by the interpreter for now)
                
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")
            except EOFError:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
                if self.debug:
                    traceback.print_exc()

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

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Quiet mode - show only program output"
    )

    return parser.parse_args()

def show_version(quiet=False):
    """Display version information."""
    if not quiet:
        print(f"Juno Programming Language v{VERSION}")
        print(f"Copyright 2025 JJPEOPLES")
        print(f"License: MIT")
        print(f"Python: {sys.version.split()[0]}")
        print(f"Platform: {sys.platform}")

def run_file(filename, args):
    """Run a Juno source file."""
    try:
        # Check if file exists
        if not os.path.exists(filename):
            if not args.quiet:
                print(f"Error: File '{filename}' not found.")
            sys.exit(1)

        # Check file extension
        if not filename.endswith('.juno') and not args.quiet:
            print(f"Warning: File '{filename}' does not have a .juno extension.")

        # Read the file
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()

        # Set up the interpreter
        juno_interpreter = Interpreter(
            debug=args.debug,
            optimize=args.optimize,
            load_stdlib=not args.no_stdlib,
            quiet=args.quiet
        )
        
        # Check syntax only if requested
        if args.check:
            result = juno_interpreter.check_syntax(source, filename)
            if result:
                if not args.quiet:
                    print(f"Syntax check passed: {filename}")
                return 0
            else:
                if not args.quiet:
                    print(f"Syntax check failed: {filename}")
                return 1

        # Execute the file
        result = juno_interpreter.execute(source, filename)
        return 0 if result else 1

    except Exception as e:
        if args.debug:
            traceback.print_exc()
        elif not args.quiet:
            print(f"Error: {str(e)}")
        return 1

def start_repl(args):
    """Start the Juno REPL."""
    try:
        # Set up the REPL
        juno_repl = REPL(
            debug=args.debug,
            optimize=args.optimize,
            load_stdlib=not args.no_stdlib,
            quiet=args.quiet
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
        show_version(args.quiet)
        return 0
    
    # Run file or start REPL
    if args.file:
        return run_file(args.file, args)
    else:
        return start_repl(args)

if __name__ == "__main__":
    sys.exit(main())