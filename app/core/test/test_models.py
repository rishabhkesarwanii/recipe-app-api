"""
Test for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model #helper func from django to get deafult user model
# it is good to use get_user_model instead of importing User model directly because if we change the user model in future it will be easy to change it 


class ModelsTests(TestCase):
    """Test for models"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email) #check if email is same as the one we passed in
        self.assertTrue(user.check_password(password)) #check if password is same as the one we passed in (check_password is a helper func from django as we are not storing password in plain text)) 