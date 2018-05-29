#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cshc.settings.local")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    # Force the use of the S3 settings if we're running the 'print_mail' management
    # command and we haven't specified a settings file on the command line.
    argv = sys.argv
    try:
        if argv[1] == 'print_mail' and not any([k.startswith('--settings') for k in argv]):
            os.environ["DJANGO_SETTINGS_MODULE"] = "cshc.settings.s3"
    except IndexError:
        pass

    execute_from_command_line(argv)
