#!/usr/bin/env python3
"""
Simple Juno Import System
This module handles importing packages in the simple Juno interpreter.
"""

import os
import sys
import importlib.util

# Constants
PACKAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packages")
USER_PACKAGES_DIR = os.path.join(os.path.expanduser("~"), ".juno", "packages")

def import_package(package_name):
    """
    Import a Juno package.
    
    Args:
        package_name (str): The name of the package to import
        
    Returns:
        dict: A dictionary of modules in the package
    """
    # Check user packages first
    user_pkg_dir = os.path.join(USER_PACKAGES_DIR, package_name)
    pkg_dir = user_pkg_dir if os.path.exists(user_pkg_dir) else os.path.join(PACKAGES_DIR, package_name)
    
    if not os.path.exists(pkg_dir):
        print(f"Error: Package '{package_name}' not found.")
        return {}
    
    # Check for Python modules
    modules = {}
    
    # Look for Python modules
    for file in os.listdir(pkg_dir):
        if file.endswith('.py'):
            module_name = file[:-3]
            module_path = os.path.join(pkg_dir, file)
            
            # Import the module
            try:
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                modules[module_name] = module
            except Exception as e:
                print(f"Error importing module {module_name}: {str(e)}")
    
    return modules