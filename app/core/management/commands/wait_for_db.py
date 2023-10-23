"""
Django command to pause execution until database is available
"""
import time
from psycopg2 import OperationalError as Psycopg2Error

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand #This is the base class

class Command(BaseCommand):
    """
    Django command to pause execution until database is available
    """
    def handle (self, *args, **options):
        """Entry point for command"""
        self.stdout.write('Waiting for database...')  #Standard out to log things to console
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default']) #This is the check method we defined in our Test
                # When we call this and db is not ready it will through a exception
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))