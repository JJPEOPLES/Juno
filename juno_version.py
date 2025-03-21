#!/usr/bin/env python3
"""
Juno Version Information
This script displays detailed version information for the Juno programming language.
"""

import os
import sys
import platform
import importlib.util
from pathlib import Path

# Default version if we can't find the version file
DEFAULT_VERSION = "2.0.10"

def get_juno_version():
    """Get the Juno version from various possible sources."""
    # Try to import from juno.version
    try:
        spec = importlib.util.find_spec("juno.version")
        if spec is not None:
            version_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(version_module)
            return version_module.VERSION
    except:
        pass
    
    # Try to import from juno package
    try:
        spec = importlib.util.find_spec("juno")
        if spec is not None:
            juno_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(juno_module)
            if hasattr(juno_module, "__version__"):
                return juno_module.__version__
    except:
        pass
    
    # Try to read from juno_standalone.py
    try:
        juno_home = os.environ.get("JUNO_HOME", os.path.dirname(os.path.abspath(__file__)))
        standalone_path = os.path.join(juno_home, "juno_standalone.py")
        
        if os.path.exists(standalone_path):
            with open(standalone_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("VERSION = "):
                        version = line.split("=")[1].strip().strip('"\'')
                        return version
    except:
        pass
    
    # Try to read from .juno/config.json
    try:
        config_path = os.path.expanduser("~/.juno/config.json")
        if os.path.exists(config_path):
            import json
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                if "version" in config:
                    return config["version"]
    except:
        pass
    
    # Return default version if all else fails
    return DEFAULT_VERSION

def get_jit_version():
    """Get the JIT compiler version if available."""
    try:
        spec = importlib.util.find_spec("juno.compiler")
        if spec is not None:
            compiler_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(compiler_module)
            if hasattr(compiler_module, "__version__"):
                return compiler_module.__version__
    except:
        pass
    
    return "Not available"

def get_framework_versions():
    """Get versions of installed Juno frameworks."""
    frameworks = {}
    
    # Check for React framework
    try:
        spec = importlib.util.find_spec("juno.frameworks.react")
        if spec is not None:
            react_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(react_module)
            if hasattr(react_module, "__version__"):
                frameworks["React"] = react_module.__version__
    except:
        pass
    
    # Check for AI framework
    try:
        spec = importlib.util.find_spec("juno.frameworks.ai")
        if spec is not None:
            ai_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(ai_module)
            if hasattr(ai_module, "__version__"):
                frameworks["AI"] = ai_module.__version__
    except:
        pass
    
    return frameworks

def show_version_info():
    """Display detailed version information."""
    juno_version = get_juno_version()
    jit_version = get_jit_version()
    frameworks = get_framework_versions()
    
    print(f"Juno Programming Language v{juno_version}")
    print(f"Copyright 2025 JJPEOPLES")
    print(f"License: MIT")
    print(f"JIT Compiler: {jit_version}")
    
    if frameworks:
        print("\nFrameworks:")
        for name, version in frameworks.items():
            print(f"  {name}: v{version}")
    
    print("\nSystem Information:")
    print(f"  Python: {platform.python_version()}")
    print(f"  Platform: {platform.platform()}")
    print(f"  OS: {platform.system()} {platform.release()}")

if __name__ == "__main__":
    show_version_info()