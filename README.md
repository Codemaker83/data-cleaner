data-cleaner
============

A temporal Repo to delete old files from a backup dir

## cleaner

To clean a backup dir you must execute::

    python cleaner.py -p path_to_backup_dir -L maximum_days_allowed

If path_to_backup_dir omitted, current dir will be assumed.
maximum_days_allowed is 15 days by default.
Optional argument --loglevel is INFO by default.
Optional argument --logfile is None bye default.
