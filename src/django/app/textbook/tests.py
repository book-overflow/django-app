from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from shared.models import University, Student, Textbook, Author, TextbookCopy, Transaction, Course
from django.contrib.gis.geos import Point

User = get_user_model()

class SharedModelsTestCase(TestCase):
    def setUp(self):
        self.university = University.objects.create(
            domain="example.edu",
            name="Example University",
            location=Point(1, 1)
        )
        self.user = User.objects.create_user(
            email="user@example.edu", password="password123"
        )
        self.student = Student.objects.create(
            email="student@example.edu",
            first_name="Test",
            last_name="Student",
            password="password",
            _university=self.university
        )
        self.author = Author.objects.create(
            first_name="John",
            last_name="Doe"
        )
        self.textbook = Textbook.objects.create(
            isbn=1234567890,
            title="Sample Textbook",
            edition=1
        )
        self.textbook._authors.add(self.author)
        self.course = Course.objects.create(
            course_number="101",
            name="Intro to Testing",
            description="A course on test-driven development.",
            _university=self.university
        )
        self.textbook._belongs.add(self.course)
        self.textbook_copy = TextbookCopy.objects.create(
            _textbook=self.textbook,
            _seller=self.student,
            condition="GOOD",
            for_rent=True,
            for_sale=True,
            sale_price=100.00,
            rent_price=10.00
        )

### Test Cases for Models

```python
    def test_student_email_domain_validation(self):
        """ Test that the Student model validates the email domain matches the university domain. """
        with self.assertRaises(ValidationError):
            Student.objects.create(
                email="invalid@student.com",
                first_name="Invalid",
                last_name="Student",
                password="password",
                _university=self.university
            )

    def test_textbook_creation(self):
        """ Test successful textbook creation. """
        self.assertIsInstance(self.textbook, Textbook)
        self.assertEqual(self.textbook.title, "Sample Textbook")

    def test_textbookcopy_price_validation(self):
        """ Test that TextbookCopy model does not allow null prices when for_sale is True. """
        with self.assertRaises(ValidationError):
            TextbookCopy.objects.create(
                _textbook=self.textbook,
                _seller=self.student,
                condition="NEW",
                for_sale=True,
                sale_price=None  # This should raise an error
            )

    def test_transaction_complete(self):
        """ Test the creation of a complete sale transaction. """
        buyer = Student.objects.create(
            email="buyer@example.edu",
            first_name="Buyer",
            last_name="User",
            password="password",
            _university=self.university
        )
        transaction = Transaction.objects.create(
            _buyer=buyer,
            _seller=self.student,
            _textbook_copy=self.textbook_copy,
            for_sale=True,
            price=100.00,
            status="COMPLETED"
        )
        self.assertEqual(transaction.status, "COMPLETED")
        self.assertEqual(transaction._buyer, buyer)
