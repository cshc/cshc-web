
from os import path
from datetime import datetime
from django.core.management.base import BaseCommand
from django.core.files import File
from documents.models import Document
from offers.models import MemberOffer

# The root directory
root = path.join(path.dirname(path.abspath(__file__)), '..', '..', '..')


def doc(*paths):
    """ Return the absolute document path """
    return path.join(root, 'static', 'documents', *paths)


def image(*paths):
    """ Return the absolute offer image path """
    return path.join(root, 'static', 'img', 'offers', *paths)


# List of all documents to initialize the datebase with. Note that some of them are already populated (e.g. with descriptions)
# in fixtures/documents.json
docs = [
    {'id': 2, 'file': doc('CSHC_Constitution_June_2017.pdf'),
     'timestamp': '2017-06-01'},
    {'id': 3, 'file': doc('CSHC_Player_Registration.pdf')},
    {'id': 4, 'file': doc('CSHC_2015_16_Accounts.pdf'),
     'timestamp': '2016-05-01'},
    {'id': 5, 'file': doc('CSHC_2014_15_Accounts.pdf'),
     'timestamp': '2015-05-01'},
    {'id': 6, 'file': doc('CSHC_Cmte_Jan_2017_Minutes.pdf'),
     'timestamp': '2017-01-01'},
    {'id': 7, 'file': doc('CSHC_AGM_2017_Minutes.pdf'),
     'timestamp': '2017-07-01'},
    {'id': 8, 'file': doc('Juniors', 'CSHC_Junior_Registration.pdf')},
    {'id': 9, 'file': doc(
        'Juniors', 'CSHC_Safeguarding_Protecting_Policy.pdf')},
    {'id': 10, 'file': doc(
        'Juniors', 'CSHC_Safeguarding_Protecting_Commitment.pdf')},
    {'id': 11, 'file': doc('Juniors', 'CSHC_Reporting_Procedures.pdf')},
    {'id': 12, 'file': doc('Juniors', 'CSHC_Photography_Guidance.pdf')},
    {'id': 15, 'title': 'CSHC AGM 2016', 'category_id': 3, 'file': doc(
        'CSHC_AGM_2016_Minutes.pdf'), 'timestamp': '2016-07-01'},
    {'id': 16, 'title': 'CSHC AGM 2014', 'category_id': 3, 'file': doc(
        'CSHC_AGM_2014_Minutes.pdf'), 'timestamp': '2014-07-01'},
    {'id': 17, 'title': 'CSHC AGM 2013', 'category_id': 3, 'file': doc(
        'CSHC_AGM_2013_Minutes.pdf'), 'timestamp': '2013-07-01'},
    {'id': 18, 'title': 'CSHC AGM 2012', 'category_id': 3, 'file': doc(
        'CSHC_AGM_2012_Minutes.pdf'), 'timestamp': '2012-07-01'},
    {'id': 19, 'title': 'CSHC AGM 2011', 'category_id': 3, 'file': doc(
        'CSHC_AGM_2011_Minutes.pdf'), 'timestamp': '2011-07-01'},
    {'id': 20, 'title': 'CSHC AGM 2010', 'category_id': 3, 'file': doc(
        'CSHC_AGM_2010_Minutes.pdf'), 'timestamp': '2010-07-01'},
    {'id': 21, 'title': 'Men\'s EGM 2009', 'category_id': 3, 'file': doc(
        'CSMHC_EGM_2009_Minutes.pdf'), 'timestamp': '2009-07-03'},
    {'id': 22, 'title': 'Ladies\' EGM 2009', 'category_id': 3, 'file': doc(
        'CSLHC_EGM_2009_Minutes.pdf'), 'timestamp': '2009-07-02'},
    {'id': 23, 'title': 'Men\'s AGM 2009', 'category_id': 3, 'file': doc(
        'CSMHC_AGM_2009_Minutes.pdf'), 'timestamp': '2009-07-01'},
    {'id': 24, 'title': 'Men\'s AGM 2003', 'category_id': 3, 'file': doc(
        'CSHC_Mens_2003_AGM_Minutes.pdf'), 'timestamp': '2003-07-01'},
    {'id': 25, 'title': 'November 2017', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Nov_2017_Minutes.pdf'), 'timestamp': '2017-11-01'},
    {'id': 26, 'title': 'September 2017', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Sep_2017_Minutes.pdf'), 'timestamp': '2017-09-01'},
    {'id': 27, 'title': 'May 2017', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_May_2017_Minutes.pdf'), 'timestamp': '2017-05-01'},
    {'id': 29, 'title': 'November 2016', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Nov_2016_Minutes.pdf'), 'timestamp': '2016-11-01'},
    {'id': 30, 'title': 'May 2016', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_May_2016_Minutes.pdf'), 'timestamp': '2016-05-01'},
    {'id': 31, 'title': 'January 2016', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Jan_2016_Minutes.pdf'), 'timestamp': '2016-01-01'},
    {'id': 32, 'title': 'November 2015', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Nov_2015_Minutes.pdf'), 'timestamp': '2015-11-01'},
    {'id': 33, 'title': 'June 2015', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Jun_2015_Minutes.pdf'), 'timestamp': '2015-06-01'},
    {'id': 34, 'title': 'April 2014', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Apr_2014_Minutes.pdf'), 'timestamp': '2014-04-01'},
    {'id': 35, 'title': 'May 2013', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_May_2013_Minutes.pdf'), 'timestamp': '2013-05-01'},
    {'id': 36, 'title': 'April 2012', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Apr_2012_Minutes.pdf'), 'timestamp': '2012-04-01'},
    {'id': 37, 'title': 'January 2012', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Jan_2012_Minutes.pdf'), 'timestamp': '2012-01-01'},
    {'id': 38, 'title': 'April 2011', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Apr_2011_Minutes.pdf'), 'timestamp': '2011-04-01'},
    {'id': 39, 'title': 'December 2010', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Dec_2010_Minutes.pdf'), 'timestamp': '2010-12-01'},
    {'id': 40, 'title': 'September 2010', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Sep_2010_Minutes.pdf'), 'timestamp': '2010-09-01'},
    {'id': 41, 'title': 'June 2010', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Jun_2010_Minutes.pdf'), 'timestamp': '2010-06-01'},
    {'id': 42, 'title': 'January 2010', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Jan_2010_Minutes.pdf'), 'timestamp': '2010-01-01'},
    {'id': 43, 'title': 'Febuary 2009', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Feb_2009_Minutes.pdf'), 'timestamp': '2009-02-01'},
    {'id': 44, 'title': 'Club Accounts 2013-14', 'category_id': 4,
        'file': doc('CSHC_2013_14_Accounts.pdf'), 'timestamp': '2014-05-01'},
    {'id': 45, 'title': 'Club Accounts 2012-13', 'category_id': 4,
        'file': doc('CSHC_2012_13_Accounts.pdf'), 'timestamp': '2013-05-01'},
    {'id': 46, 'title': 'Club Accounts 2011-12', 'category_id': 4,
        'file': doc('CSHC_2011_12_Accounts.pdf'), 'timestamp': '2012-05-01'},
    {'id': 47, 'title': 'Club Accounts 2010-11 (Ladies)', 'category_id': 4, 'file': doc(
        'CSHC_2010_11_Accounts_Ladies.pdf'), 'timestamp': '2011-05-02'},
    {'id': 48, 'title': 'Club Accounts 2010-11 (Mens)', 'category_id': 4, 'file': doc(
        'CSHC_2010_11_Accounts_Men.pdf'), 'timestamp': '2011-05-01'},
    {'id': 49, 'title': 'Club Accounts 2009-10 (Ladies)', 'category_id': 4, 'file': doc(
        'CSHC_2009_10_Accounts_Ladies.pdf'), 'timestamp': '2010-05-01'},
    {'id': 50, 'title': 'Club Accounts 2008-09 (Ladies)', 'category_id': 4, 'file': doc(
        'CSHC_2008_09_Accounts_Ladies.pdf'), 'timestamp': '2009-05-01'},
    {'id': 51, 'title': 'January 2018', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Jan_2018_Minutes.pdf'), 'timestamp': '2018-01-01'},
    {'id': 52, 'title': 'March 2017', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Mar_2017_Minutes.pdf'), 'timestamp': '2017-03-01'},
    {'id': 53, 'title': 'September 2016', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Sep_2016_Minutes.pdf'), 'timestamp': '2016-09-01'},
    {'id': 54, 'title': 'SMHC AGM 1998', 'category_id': 3, 'file': doc(
        'SMHC_AGM_1998_Minutes.pdf'), 'timestamp': '1998-07-01'},
    {'id': 55, 'title': 'SMHC AGM 1997', 'category_id': 3, 'file': doc(
        'SMHC_AGM_1997_Minutes.pdf'), 'timestamp': '1997-07-01'},
    {'id': 56, 'title': 'SMHC Newsletter April 1997', 'category_id': 7,
        'file': doc('SMHC_Newsletter_Apr_1997.pdf'), 'timestamp': '1997-04-01'},
    {'id': 57, 'title': 'SMHC Newsletter December 1997', 'category_id': 7,
        'file': doc('SMHC_Newsletter_Dec_1997.pdf'), 'timestamp': '1997-12-01'},
    {'id': 58, 'title': 'SMHC Newsletter January 1997', 'category_id': 7,
        'file': doc('SMHC_Newsletter_Jan_1997.pdf'), 'timestamp': '1997-01-01'},
    {'id': 59, 'title': 'SMHC Newsletter November 1997', 'category_id': 7,
        'file': doc('SMHC_Newsletter_Nov_1997.pdf'), 'timestamp': '1997-11-01'},
    {'id': 61, 'title': 'Club Accounts 2016-17', 'category_id': 4,
        'file': doc('CSHC_2016_17_Accounts.pdf'), 'timestamp': '2017-05-01'},
    {'id': 62, 'title': 'CSHC AGM 2015', 'category_id': 3, 'file': doc(
        'CSHC_AGM_2015_Minutes.pdf'), 'timestamp': '2015-07-01'},
    {'id': 63, 'title': 'March 2018', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Mar_2018_Minutes.pdf'), 'timestamp': '2018-04-01'},
    {'id': 64, 'title': 'CSHC AGM 2018', 'category_id': 3, 'file': doc(
        'CSHC_AGM_2018_Minutes.pdf'), 'timestamp': '2018-06-26'},
    {'id': 65, 'title': 'September 2018', 'category_id': 2, 'file': doc(
        'CSHC_Cmte_Sep_2018_Minutes.pdf'), 'timestamp': '2018-09-13'},
]

offers = [
    {'id': 1, 'image': image('Nutritionist.png')},
    {'id': 2, 'image': image('Active_Sports_Bras.gif')},
    {'id': 3, 'image': image('InjuryActive.png')},
    {'id': 4, 'image': image('Cambridge-Sport-Massage.png')},
    {'id': 5, 'image': image('LogoMiSEC.png')},
    {'id': 6, 'image': image('grove_banner.png')},
]


class Command(BaseCommand):

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, *args, **options):
        # Upload files from the static directory
        for document in docs:
            doc_obj, created = Document.objects.get_or_create(
                id=document['id'], defaults=document)
            with open(document['file'], 'rb') as f:
                document_file = File(f)
                doc_obj.file.save(path.basename(
                    document['file']), document_file, save=True)
            if document.get('timestamp', None):
                doc_obj.timestamp = datetime.strptime(
                    document['timestamp'] + ' +0000', '%Y-%m-%d %z')
            doc_obj.save()
            print('{} {}'.format('Created' if created else 'Updated', doc_obj.file))

        # Upload images for member offers
        for offer in offers:
            offer_obj = MemberOffer.objects.get(id=offer['id'])
            with open(offer['image'], 'rb') as f:
                offer_image = File(f)
                offer_obj.image.save(path.basename(
                    offer['image']), offer_image, save=True)
            offer_obj.save()
            print('Updated {}'.format(offer_obj.image))
