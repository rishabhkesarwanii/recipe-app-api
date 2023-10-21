"""
Test custom management commands
"""
from unittest.mock import patch #Mock the beahvior of the data base

from psycopg2 import OperationalError as Psycopg2Error #Psycopg2Error is the exception that is raised for errors related to the database

from django.core.management import call_command #call_command is a helper function for calling commands from the command line by its name
from django.db.utils import OperationalError #OperationalError is the exception that is raised when the database is not available
from django.test import SimpleTestCase

@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test Commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for db when db is available"""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])
    
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db when getting OperationalError"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True] 
        
        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])