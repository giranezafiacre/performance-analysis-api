from django.test import TestCase

from app.models import BackgroundStudy, File, Student
from django.shortcuts import  get_object_or_404

class StudentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # background=get_object_or_404(BackgroundStudy, id=1)
        Student.objects.create(fname='Fiacre Giraneza', gender='1',healthStatus='1',program='1')

    def test_full_name_label(self):
        student = Student.objects.get(id=1)
        field_label = student._meta.get_field('fname').verbose_name
        self.assertEqual(field_label, 'fname')

    def test_program_label(self):
        student = Student.objects.get(id=1)
        field_label = student._meta.get_field('program').verbose_name
        self.assertEqual(field_label, 'program')

    def test_fname_max_length(self):
        student = Student.objects.get(id=1)
        max_length = Student._meta.get_field('fname').max_length
        self.assertEqual(max_length, 30)

    def test_object_name_is_fname(self):
        student = Student.objects.get(id=1)
        expected_object_name = f'{student.fname}'
        self.assertEqual(str(student), expected_object_name)




