from django.test import TestCase
import unittest
from django.test import Client
from django.urls import reverse
from .models import Textbook

# Create your tests here.
class TextbookViewsTestCase(unittest.TestCase):
    def setUp(self):
        # Create some example textbooks for testing
        Textbook.objects.create(title="Test Textbook 1", author="Author 1")
        Textbook.objects.create(title="Test Textbook 2", author="Author 2")

    def test_textbook_list_view(self):
        # Initialize Django test client
        client = Client()
        # Make GET request to textbook list view
        response = client.get(reverse('textbook_list'))
        # Check if response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if the list of textbooks is rendered in the response
        self.assertQuerysetEqual(
            response.context['textbooks'],
            ['<Textbook: Test Textbook 1>', '<Textbook: Test Textbook 2>']
        )

    def test_textbook_detail_view(self):
        # Get the ID of the first textbook
        textbook_id = Textbook.objects.first().id
        # Initialize Django test client
        client = Client()
        # Make GET request to textbook detail view
        response = client.get(reverse('textbook_detail', args=[textbook_id]))
        # Check if response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if the correct textbook details are rendered in the response
        self.assertContains(response, "Test Textbook 1")
        self.assertContains(response, "Author 1")
