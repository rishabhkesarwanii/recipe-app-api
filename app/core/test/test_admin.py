"""
Test for Django admin modifications
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Test for Django admin modifications"""

    def setUp(self): #setUp is a function that is ran before every test that we run (it is a helper function from TestCase class)
        """Setup for tests"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = "admin@example.com",
            password = "test123"
        )
        self.client.force_login(self.admin_user) #force_login is a helper function from TestCase class
        self.user = get_user_model().objects.create_user(
            email = "user@example.com",
            password = "test123",
            name = "Test User"
        )
    
    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist') #reverse is a helper function from django to generate urls for admin page 
        res = self.client.get(url) #res is a response object

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
    
    def test_edit_user_page(self):
        """Test that the edit user page works"""
        url = reverse('admin:core_user_change', args=[self.user.id]) #args is a list of arguments that we want to pass in the url (in this case we want to pass the user id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200) #200 is the status code for OK
    
    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)