#!/usr/bin/env python3
"""
Juno Package Manager (JPM)
A simple package manager for Juno.
"""

import os
import sys
import json
import shutil
import argparse
import zipfile
import tempfile
from pathlib import Path

# Constants
JPM_VERSION = "1.0.0"
PACKAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packages")
USER_PACKAGES_DIR = os.path.join(os.path.expanduser("~"), ".juno", "packages")

def ensure_dirs():
    """Ensure package directories exist."""
    os.makedirs(USER_PACKAGES_DIR, exist_ok=True)

def list_packages():
    """List all available packages."""
    print("Available packages:")
    
    # Check built-in packages
    if os.path.exists(PACKAGES_DIR):
        for pkg in os.listdir(PACKAGES_DIR):
            pkg_dir = os.path.join(PACKAGES_DIR, pkg)
            if os.path.isdir(pkg_dir):
                pkg_json = os.path.join(pkg_dir, "package.json")
                if os.path.exists(pkg_json):
                    try:
                        with open(pkg_json, 'r') as f:
                            pkg_info = json.load(f)
                        print(f"  {pkg_info.get('name', pkg)} (v{pkg_info.get('version', '?')}) - {pkg_info.get('description', 'No description')}")
                    except:
                        print(f"  {pkg} (unknown version) - Could not read package info")
    
    # Check user packages
    if os.path.exists(USER_PACKAGES_DIR):
        for pkg in os.listdir(USER_PACKAGES_DIR):
            pkg_dir = os.path.join(USER_PACKAGES_DIR, pkg)
            if os.path.isdir(pkg_dir):
                pkg_json = os.path.join(pkg_dir, "package.json")
                if os.path.exists(pkg_json):
                    try:
                        with open(pkg_json, 'r') as f:
                            pkg_info = json.load(f)
                        print(f"  {pkg_info.get('name', pkg)} (v{pkg_info.get('version', '?')}) [user] - {pkg_info.get('description', 'No description')}")
                    except:
                        print(f"  {pkg} (unknown version) [user] - Could not read package info")

def install_package(package_name):
    """Install a package."""
    ensure_dirs()
    
    # Check if package exists in built-in packages
    pkg_dir = os.path.join(PACKAGES_DIR, package_name)
    if os.path.exists(pkg_dir) and os.path.isdir(pkg_dir):
        # Copy package to user packages
        user_pkg_dir = os.path.join(USER_PACKAGES_DIR, package_name)
        if os.path.exists(user_pkg_dir):
            print(f"Package '{package_name}' is already installed. Use 'jpm update {package_name}' to update.")
            return
        
        # Copy package files
        shutil.copytree(pkg_dir, user_pkg_dir)
        print(f"Package '{package_name}' installed successfully.")
    else:
        print(f"Package '{package_name}' not found.")

def uninstall_package(package_name):
    """Uninstall a package."""
    user_pkg_dir = os.path.join(USER_PACKAGES_DIR, package_name)
    if os.path.exists(user_pkg_dir) and os.path.isdir(user_pkg_dir):
        shutil.rmtree(user_pkg_dir)
        print(f"Package '{package_name}' uninstalled successfully.")
    else:
        print(f"Package '{package_name}' is not installed.")

def update_package(package_name):
    """Update a package."""
    # First uninstall
    uninstall_package(package_name)
    # Then install
    install_package(package_name)
    print(f"Package '{package_name}' updated successfully.")

def show_package_info(package_name):
    """Show package information."""
    # Check user packages first
    user_pkg_dir = os.path.join(USER_PACKAGES_DIR, package_name)
    pkg_dir = user_pkg_dir if os.path.exists(user_pkg_dir) else os.path.join(PACKAGES_DIR, package_name)
    
    if os.path.exists(pkg_dir) and os.path.isdir(pkg_dir):
        pkg_json = os.path.join(pkg_dir, "package.json")
        readme = os.path.join(pkg_dir, "README.md")
        
        if os.path.exists(pkg_json):
            try:
                with open(pkg_json, 'r') as f:
                    pkg_info = json.load(f)
                
                print(f"Package: {pkg_info.get('name', package_name)}")
                print(f"Version: {pkg_info.get('version', 'unknown')}")
                print(f"Description: {pkg_info.get('description', 'No description')}")
                print(f"Author: {pkg_info.get('author', 'Unknown')}")
                print(f"License: {pkg_info.get('license', 'Unknown')}")
                
                if 'dependencies' in pkg_info and pkg_info['dependencies']:
                    print("\nDependencies:")
                    for dep, ver in pkg_info['dependencies'].items():
                        print(f"  {dep}: {ver}")
                
                if 'keywords' in pkg_info and pkg_info['keywords']:
                    print("\nKeywords:")
                    print(f"  {', '.join(pkg_info['keywords'])}")
                
                if os.path.exists(readme):
                    print("\nREADME:")
                    with open(readme, 'r') as f:
                        readme_content = f.read()
                    print(f"\n{readme_content[:500]}...")
                    print("\nUse 'jpm readme {package_name}' to view the full README.")
            except Exception as e:
                print(f"Error reading package info: {str(e)}")
        else:
            print(f"Package '{package_name}' does not have a package.json file.")
    else:
        print(f"Package '{package_name}' not found.")

def show_readme(package_name):
    """Show the package README."""
    # Check user packages first
    user_pkg_dir = os.path.join(USER_PACKAGES_DIR, package_name)
    pkg_dir = user_pkg_dir if os.path.exists(user_pkg_dir) else os.path.join(PACKAGES_DIR, package_name)
    
    if os.path.exists(pkg_dir) and os.path.isdir(pkg_dir):
        readme = os.path.join(pkg_dir, "README.md")
        
        if os.path.exists(readme):
            with open(readme, 'r') as f:
                readme_content = f.read()
            print(f"\n{readme_content}")
        else:
            print(f"Package '{package_name}' does not have a README.md file.")
    else:
        print(f"Package '{package_name}' not found.")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Juno Package Manager")
    
    parser.add_argument("--version", action="store_true", help="Show version information")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available packages")
    
    # Install command
    install_parser = subparsers.add_parser("install", help="Install a package")
    install_parser.add_argument("package", help="Package name")
    
    # Uninstall command
    uninstall_parser = subparsers.add_parser("uninstall", help="Uninstall a package")
    uninstall_parser.add_argument("package", help="Package name")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update a package")
    update_parser.add_argument("package", help="Package name")
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Show package information")
    info_parser.add_argument("package", help="Package name")
    
    # Readme command
    readme_parser = subparsers.add_parser("readme", help="Show package README")
    readme_parser.add_argument("package", help="Package name")
    
    args = parser.parse_args()
    
    if args.version:
        print(f"Juno Package Manager v{JPM_VERSION}")
        return 0
    
    if args.command == "list":
        list_packages()
    elif args.command == "install":
        install_package(args.package)
    elif args.command == "uninstall":
        uninstall_package(args.package)
    elif args.command == "update":
        update_package(args.package)
    elif args.command == "info":
        show_package_info(args.package)
    elif args.command == "readme":
        show_readme(args.package)
    else:
        parser.print_help()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())