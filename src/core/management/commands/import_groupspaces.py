"""
Tool to migrate/sync data from Group Spaces into the CSHC website database.

Mainly targets the Member model.

Usage: "python manage.py import_groupspaces export.csv"

Notes:
- export.csv is generated from this page: http://groupspaces.com/cambridgesouthhockeyclub/manage/members/export/
- export.csv should contain the column names in the first row

"""
import os
import traceback
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db.models import Q
from members.models import Member
from core.models import Gender


class Command(BaseCommand):
    help = "Migration of member data from a CSV file exported from GroupSpaces."

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file', help='The CSV file to import group spaces data from')
        parser.add_argument(
            '--sim',
            action='store_true',
            dest='sim',
            default=False,
            help='Simulation mode (database will not be written to)',
        )

    def __init__(self):
        self._options = None
        self._headerRow = None
        super(Command, self).__init__()

    def parse_file(self):
        """ Parse the whole CSV file into a list or (parsed) rows """
        rows = []
        cols = {}
        with open(self._options['csv_file'], newline='') as source_file:
            reader = csv.reader(source_file)
            try:
                for row in reader:
                    if not cols:
                        self._headerRow = row
                        for index in range(0, len(row)):
                            cols[row[index]] = index
                    else:
                        parsed_row = self.parse_row(row)
                        # Ignore parents
                        if not parsed_row['Junior Player\'s Name (1)']:
                            rows.append(self.parse_row(row))
            except:
                traceback.print_exc()
        return rows

    def parse_row(self, row):
        """ Parse a single row of CSV data """
        parsed_row = {}
        for index in range(0, len(row)):
            parsed_row[self._headerRow[index]
                       ] = row[index].strip() if row[index] != '' else None
        parsed_row['Full Name'] = "{} {}".format(
            parsed_row['Forename'], parsed_row['Surname'])
        parsed_row['Umpire'] = True if parsed_row['Umpire'] and parsed_row['Umpire'].lower(
        ) == 'yes' else False
        parsed_row['Coach'] = True if parsed_row['Coach'] and parsed_row['Coach'].lower(
        ) == 'yes' else False
        parsed_row['Date of Birth'] = datetime.strptime(
            parsed_row['Date of Birth'] + ' +0000', '%d %b %Y %z').date() if parsed_row['Date of Birth'] is not None else None
        return parsed_row

    def found(self, row_data, member):
        """ 
        Handle a row of data that has a single matching member. 

        Updates the corresponding fields in the Member object.
        """
        if member.email and row_data['E-mail Address'] and (member.email != row_data['E-mail Address']):
            print('WARNING - email discrepancy: {} vs {}'.format(
                member.email, row_data['E-mail Address']))
        elif row_data['E-mail Address']:
            member.email = row_data['E-mail Address']

        member.is_umpire = row_data['Umpire']
        member.is_coach = row_data['Coach']

        if row_data['Phone Number']:
            member.phone = row_data['Phone Number']

        if row_data['Date of Birth']:
            member.dob = row_data['Date of Birth']

        if row_data['Address (street)']:
            member.addr_street = row_data['Address (street)']
        if row_data['Address (line 2)']:
            member.addr_line2 = row_data['Address (line 2)']
        if row_data['Address (town)']:
            member.addr_town = row_data['Address (town)']
        if row_data['Post Code']:
            member.addr_postcode = row_data['Post Code']

        if row_data['Emergency Contact (name)']:
            member.emergency_contact = row_data['Emergency Contact (name)']
        if row_data['Emergency Contact (relationship)']:
            member.emergency_relationship = row_data['Emergency Contact (relationship)']
        if row_data['Emergency Contact (phone)']:
            member.emergency_phone = row_data['Emergency Contact (phone)']
        if row_data['Relevant Medical Details']:
            member.medical_notes = row_data['Relevant Medical Details']

        if not self._options['sim']:
            member.save()

        return member.full_name()

    def not_found(self, row_data):
        suggestions = Member.objects.filter(
            last_name=row_data['Surname'], gender=getattr(Gender, row_data['Gender']))
        not_found_text = row_data['Full Name']
        if len(suggestions):
            not_found_text += " (Suggestions: {})".format(
                ", ".join([s.full_name() for s in suggestions]))
        return not_found_text

    def handle(self, *args, **options):
        if not os.path.isfile(options['csv_file']):
            print("ERROR: No such file {}".format(options['csv_file']))
            return

        self._options = options

        names = []
        duplicates = []
        found = []
        not_found = []
        multiple_matches = []

        parsed_rows = self.parse_file()

        # First we need to check for duplicate names and cache them. When we import, we'll skip these and log them so the
        # admin can handle them manually.
        for row_data in parsed_rows:
            if row_data['Full Name'] in names:
                duplicates.append(row_data['Full Name'])
            names.append(row_data['Full Name'])
        duplicates = list(set(duplicates))
        for duplicate in duplicates:
            parsed_rows = [
                r for r in parsed_rows if r['Full Name'] != duplicate]

        # Then we go through the parsed data and try to update matching members
        for row_data in parsed_rows:
            try:
                first_name_query = Q(first_name=row_data['Forename']) | Q(
                    known_as=row_data['Forename'])
                matching_members = Member.objects.filter(first_name_query).filter(
                    last_name=row_data['Surname'], gender=getattr(Gender, row_data['Gender']))
                if len(matching_members) == 1:
                    found.append(self.found(row_data, matching_members[0]))
                elif len(matching_members) > 1:
                    # We've got multiple possible matches. Just cache them and we'll log this to the user at the end.
                    multiple_matches.append(
                        dict(name=row_data['Full Name'], matches=list(matching_members)))
                else:
                    not_found.append(self.not_found(row_data))
            except Member.DoesNotExist:
                not_found.append(self.not_found(row_data))

        for f in found:
            if self._options['sim']:
                print('Found: ' + f)
            else:
                print('Updated: ' + f)
        for nf in not_found:
            print('Not found: ' + nf)
        for mm in multiple_matches:
            print('Multiple matches for ' + mm['name'])
            for match in mm['matches']:
                print('\t{}'.format(match.full_name()))
        for d in duplicates:
            print('Duplicate: ' + d)
