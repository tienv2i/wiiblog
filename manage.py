#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

sys.dont_write_bytecode = True

load_dotenv()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiiblog.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
