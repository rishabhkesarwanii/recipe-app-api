"""
Test custom management commands
"""
from unittest.mock import patch #Mock the beahvior of the data base

from psycopg2 import OperationalError as Psycopg2Error #OperationalError is one of the error we can face while we try to connect when db is not ready (by psycopg2)

from django.core.management import call_command #call_command is a helper function for calling commands from the command line by its name
from django.db.utils import OperationalError  #One more error the database is not there or so (by django)
from django.test import SimpleTestCase

@patch('core.management.commands.wait_for_db.Command.check') # Mock the behaviour of our database    ;   Management class Baseclass has a check method
class CommandTests(SimpleTestCase):
    """Test Commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for db when db is available"""
        patched_check.return_value = True #return the mock value = True

        call_command('wait_for_db') #calling the managment command "python manage.py wait_for_db"
 
        patched_check.assert_called_once_with(databases=['default']) #Ensure we are calling right command with write databases
    
    @patch('time.sleep') #Mock the sleep behaviour (we are using this patch method becuase we dont want to wait in our test it will slow down test)
    def test_wait_for_db_delay(self, patched_sleep, patched_check): #What to check when DB is not ready
        """Test waiting for db when getting OperationalError"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True] #The first two time is we are raising Psycopg2Error Operational Error then for next 3 times Django OperationalError
        #These are simulations of some real word situations we are mocking the behaviour (2 and 3 in above expession are self assign valued for the sim)
        #The 6th time we call it it will be return true

        # Side Effect is used to raise an exception instead return a value (in this case we want to raise an exceptions that would be raised if the db is not ready)
        # Side Effect lets you pass different items that can handle different things accordingly
        # If we pass in a Exception mocking library will know to raise a exception(passing in side effect )
        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        #We want to call the method 6 times and then check for the sixth time for the true value 
        patched_check.assert_called_with(databases=['default'])