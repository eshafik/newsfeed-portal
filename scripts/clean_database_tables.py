"""
    Version: 1.0.0
    Author: MSI Shafik
"""

from django.db import connections, OperationalError

# Drop all tables from a given database

"""
python manage.py runscript clean_database_tables
"""


def run():
    primary_db = connections['default']

    try:
        primary_conn = primary_db.cursor()
    except OperationalError as err:
        print(err)
        return None

    try:
        primary_conn.execute(
            "SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_schema,table_name")
        rows = primary_conn.fetchall()
        for row in rows:
            primary_conn.execute("drop table " + row[1] + " cascade")
        primary_conn.close()
        primary_conn.close()
    except Exception as err:
        print(err)
