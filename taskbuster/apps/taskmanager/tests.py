from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from . import models

# Create your tests here.
class TestProfileModel(TestCase):

    def test_profile_creation(self):
        User = get_user_model()
        user = User.objects.create(
               username='taskbuster',
               password='TestseT')

        self.assertIsInstance(user.profile, models.Profile)

        user.save()
        self.assertIsInstance(user.profile, models.Profile)


class TestProjectModel(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username='taskbuster', password='test')
        self.profile = self.user.profile

    def tearDown(self):
        self.user.delete()

    def test_validation_color(self):
        project = models.Project(user=self.profile, name='Taskmanger')
        self.assertTrue(project.color == '#fff')
        project.full_clean()

        # Valid colors
        for color in ['#1cA', '#1256aB']:
            project.color = color
            project.full_clean()

        # Invalid colors
        for color in ['1cA', '1256aB', '#1', '#12', '#1234', '#12345',
                      '#1234567']:
            with self.assertRaises(
                 ValidationError,
                 msg="{} didn't raise a ValidationError".format(color)):
                project.color = color
                project.full_clean()
