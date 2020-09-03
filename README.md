**Cambridge South Hockey Club**
===============================

This repository contains the source code for the [Cambridge South Hockey Club website](https://www.cambridgesouthhockeyclub.co.uk).

Full documentation (work-in-progress) can be found here: [cshc.readthedocs.io](http://cshc.readthedocs.io/en/latest/index.html)

## Migrating Database from Production to Local Env

1. On the EC2 instance:

```
mysqldump --skip-extended-insert --compact --default-character-set=utf8 cshc > dump_mysql.sql
```

2. Download the `dump_mysql.sql` file to your local machine.

3. Import the database:

```
mysql -u root -p cshc < /path/to/dump_mysql.sql
```

4. Copy the media files from production to the local dev environment.

5. **IMPORTANT**: Change the URL of the single `sites` entry via the admin interface to `localhost:8000`

```
python manage.py media_copy --local
```