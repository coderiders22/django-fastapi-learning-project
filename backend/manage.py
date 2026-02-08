"""
Django's command-line utility for administrative tasks.

This file is used to run common Django commands like:
- runserver
- makemigrations
- migrate
- createsuperuser
"""

import os
import sys
from pathlib import Path


def main():
    """
    Entry point for Django management commands.
    """

    # Get the base directory (project root)
    BASE_DIR = Path(__file__).resolve().parent

    # Ensure project root is added to Python path
    # This avoids import issues when running commands
    sys.path.append(str(BASE_DIR))

    # Set default Django settings module
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    try:
        # Import Django's command executor
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Raised if Django is not installed or not found in environment
        raise ImportError(
            "Couldn't import Django. Make sure Django is installed "
            "and available in the current virtual environment."
        ) from exc

    # Execute the command passed via terminal
    execute_from_command_line(sys.argv)


# Standard Python entry point
if __name__ == "__main__":
    main()
