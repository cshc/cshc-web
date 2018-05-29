"""
Test utility to print a templated mail given the mail template and the
context (as a JSON file).

Usage:

1. Using defaults (prepared JSON context file, save mail messages to current directory):
'python manage.py print_mail -s mytemplate'

2. Specifying all options:
'python manage.py print_mail -c mycontext.json mytemplate > message.html'

Note: There is some special code in manage.py that sets the DJANGO_SETTINGS_MODULE
      to 'cshc.settings.s3' if its not set by using the --settings option on the 
      command line. This settings file ensures we have valid absolute URLs for images etc.
"""
import json
import os.path
from django.core.management.base import BaseCommand, CommandError
from templated_email import get_templated_mail


class Command(BaseCommand):
    help = (
        "Outputs the specified mail template to the console. "
        "The context for the mail should be provided by specifying "
        "a JSON file.\n"
        "e.g. python manage.py print_mail mytemplate mycontext.json > contact.html"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'template_name',
            help='The template name. This must correspond to a template file within the directory \'cshc/templates/emails\'')
        parser.add_argument(
            '-c', '--context',
            dest='context',
            help='A JSON file containing the context to pass to the template')
        parser.add_argument(
            '-s', '--auto-save',
            action='store_true',
            dest='save',
            help='If set, the mail will be saved as \'template_name.txt\' and \'template_name.html\'')

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, *args, **options):
        template_name = options.get('template_name')
        context_file = options.get('context')

        # If context file is not set, use the template name to assume the context file path
        if context_file is None:
            context_file = 'core/management/commands/mail_context/{}.json'.format(
                template_name)

        # Check that context JSON file exists
        if not os.path.isfile(context_file):
            raise CommandError('Context JSON file not found: ' + context_file)

        # Read in the context file to a dictionary
        with open(context_file) as handle:
            context = json.loads(handle.read())

        try:
            mail = get_templated_mail(
                template_name=template_name,
                from_email='from@example.com',
                to=['to@example.com'],
                context=context,
            )
        except Exception as ex:
            raise CommandError(
                'Could not get templated mail named \'{}\''.format(template_name), ex)

        # If the 'save' option (-s) was specified, save the text and HTML versions
        # of the mail message to files.
        if options.get('save'):
            main_message = mail.body
            if hasattr(mail, 'alternatives') and len(mail.alternatives):
                main_message = mail.alternatives[0][0]
                with open(template_name + '.txt', 'w') as mail_txt:
                    mail_txt.write(mail.body)

            with open(template_name + '.html', 'w') as mail_html:
                mail_html.write(main_message)
        # Otherwise, just print the HTML message to stdout
        else:
            print(mail.alternatives[0][0])
