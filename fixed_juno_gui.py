#!/usr/bin/env python3
"""
Fixed Juno GUI Library - Simple GUI support for Juno programs
This module provides basic GUI capabilities for Juno programs with improved error handling.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import threading
import queue
import time

# Global variables
_root = None
_event_queue = queue.Queue()
_windows = {}
_components = {}
_component_counter = 0

def _ensure_root():
    """Ensure the root window exists."""
    global _root
    if _root is None:
        _root = tk.Tk()
        _root.title("Juno GUI")
        _root.protocol("WM_DELETE_WINDOW", _on_root_close)
        _windows["root"] = _root

def _on_root_close():
    """Handle root window close event."""
    global _root
    if _root:
        _root.destroy()
        _root = None
        _event_queue.put(("EXIT", None))

def _process_events():
    """Process GUI events."""
    global _root
    if _root:
        _root.update()

def create_window(title="Juno Window", width=400, height=300):
    """Create a new window."""
    # Convert parameters to the right types
    if isinstance(width, str):
        width = int(width)
    if isinstance(height, str):
        height = int(height)
        
    _ensure_root()
    
    window = tk.Toplevel(_root)
    window.title(title)
    window.geometry(f"{width}x{height}")
    window.protocol("WM_DELETE_WINDOW", lambda: _on_window_close(window))
    
    window_id = f"window_{len(_windows)}"
    _windows[window_id] = window
    
    return window_id

def _on_window_close(window):
    """Handle window close event."""
    window.destroy()
    # Remove from windows dict
    for window_id, w in list(_windows.items()):
        if w == window:
            del _windows[window_id]
            break

def create_button(window_id, text, x, y, width=100, height=30):
    """Create a button."""
    global _component_counter
    
    # Convert parameters to the right types
    if isinstance(x, str):
        x = int(x)
    if isinstance(y, str):
        y = int(y)
    if isinstance(width, str):
        width = int(width)
    if isinstance(height, str):
        height = int(height)
    
    if window_id not in _windows:
        if window_id == "root":
            _ensure_root()
            window = _root
        else:
            return None
    else:
        window = _windows[window_id]
    
    button = tk.Button(window, text=text)
    button.place(x=x, y=y, width=width, height=height)
    
    component_id = f"button_{_component_counter}"
    _component_counter += 1
    
    _components[component_id] = button
    
    # Set up command
    button.config(command=lambda: _on_button_click(component_id))
    
    return component_id

def _on_button_click(component_id):
    """Handle button click event."""
    _event_queue.put(("BUTTON_CLICK", component_id))

def create_label(window_id, text, x, y, width=100, height=30):
    """Create a label."""
    global _component_counter
    
    # Convert parameters to the right types
    if isinstance(x, str):
        x = int(x)
    if isinstance(y, str):
        y = int(y)
    if isinstance(width, str):
        width = int(width)
    if isinstance(height, str):
        height = int(height)
    
    if window_id not in _windows:
        if window_id == "root":
            _ensure_root()
            window = _root
        else:
            return None
    else:
        window = _windows[window_id]
    
    label = tk.Label(window, text=text)
    label.place(x=x, y=y, width=width, height=height)
    
    component_id = f"label_{_component_counter}"
    _component_counter += 1
    
    _components[component_id] = label
    
    return component_id

def create_textfield(window_id, x, y, width=200, height=30):
    """Create a text field."""
    global _component_counter
    
    # Convert parameters to the right types
    if isinstance(x, str):
        x = int(x)
    if isinstance(y, str):
        y = int(y)
    if isinstance(width, str):
        width = int(width)
    if isinstance(height, str):
        height = int(height)
    
    if window_id not in _windows:
        if window_id == "root":
            _ensure_root()
            window = _root
        else:
            return None
    else:
        window = _windows[window_id]
    
    entry = tk.Entry(window)
    entry.place(x=x, y=y, width=width, height=height)
    
    component_id = f"textfield_{_component_counter}"
    _component_counter += 1
    
    _components[component_id] = entry
    
    return component_id

def set_text(component_id, text):
    """Set text for a component."""
    if component_id not in _components:
        return False
    
    component = _components[component_id]
    
    if isinstance(component, tk.Label):
        component.config(text=text)
    elif isinstance(component, tk.Entry):
        component.delete(0, tk.END)
        component.insert(0, text)
    elif isinstance(component, tk.Button):
        component.config(text=text)
    
    return True

def get_text(component_id):
    """Get text from a component."""
    if component_id not in _components:
        return ""
    
    component = _components[component_id]
    
    if isinstance(component, tk.Label):
        return component.cget("text")
    elif isinstance(component, tk.Entry):
        return component.get()
    elif isinstance(component, tk.Button):
        return component.cget("text")
    
    return ""

def show_message(title, message):
    """Show a message dialog."""
    _ensure_root()
    messagebox.showinfo(title, message)

def show_input_dialog(title, prompt):
    """Show an input dialog."""
    _ensure_root()
    return simpledialog.askstring(title, prompt)

def show_file_dialog(title, file_types=None):
    """Show a file dialog."""
    _ensure_root()
    if file_types is None:
        file_types = [("All files", "*.*")]
    return filedialog.askopenfilename(title=title, filetypes=file_types)

def wait_for_event(timeout=0.1):
    """Wait for a GUI event."""
    _process_events()
    
    try:
        # Convert timeout to float if it's a string
        if isinstance(timeout, str):
            timeout = float(timeout)
            
        event = _event_queue.get(block=True, timeout=timeout)
        return event
    except queue.Empty:
        return None

def start_gui():
    """Start the GUI event loop."""
    _ensure_root()
    
    # Start in a separate thread
    def gui_thread():
        while _root:
            _process_events()
            time.sleep(0.01)
    
    threading.Thread(target=gui_thread, daemon=True).start()

def stop_gui():
    """Stop the GUI event loop."""
    global _root
    if _root:
        _root.destroy()
        _root = None

# Export functions for Juno
__all__ = [
    "create_window",
    "create_button",
    "create_label",
    "create_textfield",
    "set_text",
    "get_text",
    "show_message",
    "show_input_dialog",
    "show_file_dialog",
    "wait_for_event",
    "start_gui",
    "stop_gui"
]