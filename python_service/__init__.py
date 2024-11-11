# python_service/__init__.py

from .api_manager_service import APIManagerService

# You can specify what gets exported when someone imports the package
__all__ = ['APIManagerService']

# Optional: Package metadata
__version__ = '1.0.0'
__author__ = 'Jayram Keshavan'
__description__ = 'Node-RED integration for API Manager'