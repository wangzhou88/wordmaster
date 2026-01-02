"""
Kivy compatibility fixes for Python 3.11+
"""
import sys
import os

# Fix for Kivy with Python 3.11+
try:
    from kivy.graphics import VertexInstruction
    from kivy.graphics import Mesh
except ImportError:
    # Fallback for newer Kivy versions
    from kivy.graphics import VertexFormat
    from kivy.graphics import Mesh

# Fix Kivy font loading on Android
def fix_font_paths():
    # Set Kivy fonts to system fonts on Android
    import kivy
    from kivy.core.text import Label
    from kivy.resources import resource_add_path
    
    # Set default font paths for Android
    try:
        # Try to find a compatible font
        resource_add_path('/system/fonts/')
        resource_add_path('/system/usr/fonts/')
        resource_add_path('/data/fonts/')
    except Exception as e:
        print(f"Font path setup error: {e}")

# Apply fixes
fix_font_paths()