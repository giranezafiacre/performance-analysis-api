from django.test import TestCase
from django.urls import reverse

from app.models import Student

class StudentListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Student.objects.create(
                fname=f'Christian {author_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, 200)

    
