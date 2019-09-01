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

3. Download the `mysql2sqlite` script from [here](https://github.com/dumblob/mysql2sqlite)

4. Run the script to create a new sqlite database file from the MySQL export:

```
./mysql2sqlite dump_mysql.sql | sqlite3 db.sqlite3
```

5. Replace the existing `src/db.sqlite3` file with the one created in the previous step.

6. Copy the media files from production to the local dev environment. Note this also copies them to the (unused) staging bucket.

```
python manage.py media_copy --local
```