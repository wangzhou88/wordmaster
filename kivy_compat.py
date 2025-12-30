import inspect
import os

def getmodulename(path):
    """Get the module name for a given path, or None if the path is not a module."""
    basename = os.path.basename(path)
    name, ext = os.path.splitext(basename)
    if ext == '.py':
        return name
    return None

if not hasattr(inspect, 'getmodulename'):
    inspect.getmodulename = getmodulename
