import os
import gubookhub_app.models
import tempfile
from django.test import TestCase
from django.urls import reverse, resolve
from django.db import models
from django.forms import fields as django_fields
from django.conf import settings
from gubookhub_app import forms
from gubookhub_app.models import Book
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.staticfiles import finders

def create_user_object():
    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()

    return user

class UserAuthenticationTests(TestCase):
    def test_userprofile_class(self):

        user_profile = gubookhub_app.models.User()

        expected_attributes = {
            'username': 'testuser',
            'first_name': "Test",
            'last_name': 'User',
            'email': "test@test.com",
        }

        expected_types = {
            'username': models.fields.CharField,
            'first_name': models.fields.CharField,
            'last_name': models.fields.CharField,
            'email': models.fields.EmailField,
        }

        found_count = 0

        for attr in user_profile._meta.fields:
            attr_name = attr.name

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1

                    self.assertEqual(type(attr), expected_types[attr_name], f"The type of attribute for '{attr_name}' was '{type(attr)}'; we expected '{expected_types[attr_name]}'. Check your definition of the UserProfile model.")
                    setattr(user_profile, attr_name, expected_attributes[attr_name])

        self.assertEqual(found_count, len(expected_attributes.keys()), f"In the UserProfile model, we found {found_count} attributes, but were expecting {len(expected_attributes.keys())}. Check your implementation and try again.")
        user_profile.save()

    def test_user_form(self):
        self.assertTrue('UserForm' in dir(forms), "UserForm is not present in forms.py.")

        user_form = forms.UserForm()
        self.assertEqual(type(user_form.__dict__['instance']), User, "User form does not match with user model.")

        fields = user_form.fields

        expected_fields = {
            'username': django_fields.CharField,
            'email': django_fields.EmailField,
            'password': django_fields.CharField,
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"The field {expected_field_name} was not found in the UserForm form. Check you have complied with the specification, and try again.")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"The field {expected_field_name} in UserForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.")

class StructureTests(TestCase):
    fixtures = ["tests.json", ]
    def test_base_template_exists(self):
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'gubookhub', 'base.html')
        self.assertTrue(os.path.exists(template_base_path), "Base template does not exist.")

    def test_base_template_usage(self):
        urls = [reverse('gubookhub_app:index'),
                reverse('gubookhub_app:about'),
                reverse('gubookhub_app:search'),]

        templates = ['gubookhub/index.html',
                     'gubookhub/about.html',
                     'gubookhub/search.html',]

        for url, template in zip(urls, templates):
            response = self.client.get(url)
            self.assertTemplateUsed(response, template)

class SearchTests(TestCase):
    pass;

class AddBookTests(TestCase):
    fixtures = ["tests.json", ]
    def test_add_book_functionality(self):
        form = forms.BookForm(data={'title':'Tango with Django 2', 'author':'Leif Azzopardi', "url":"https://moodle.gla.ac.uk/pluginfile.php/3433670/mod_resource/content/1/twd-uog-lib-2021-01-07.pdf", "favorite_count":0, "course":1, "user":User.objects.get(username="vertex")})

        self.assertTrue(form.is_valid(), "Form is invalid.")

    def test_add_book_functionality(self):
        form = forms.BookForm(data={'title':'Tango with Django 2', 'author':'Leif Azzopardi', "url":"https://moodle.gla.ac.uk/pluginfile.php/3433670/mod_resource/content/1/twd-uog-lib-2021-01-07.pdf", "favorite_count":0, "course":1})
        book = form.save(commit=False)
        book.user = User.objects.get(username="vertex")
        book.save()

        books = Book.objects.filter(title='Tango with Django 2')

        self.assertEqual(len(books), 1, "When adding a new book, it does not appear in the list of books after being created.")

class URLTests(TestCase):
    def test_add_book_url_mapping(self):
        try:
            resolved_name = resolve('/gubookhub_app/add_book/').view_name
        except:
            resolved_name = ''

        self.assertEqual(resolved_name, "gubookhub_app:add_book", "The lookup of URL '/gubookhub_app/add_book/' did not return a mapping name of 'gubookhub_app:add_book'.")

    def test_subject_url_mapping(self):
        try:
            resolved_url = reverse('gubookhub_app:subject', kwargs={'subject_name_slug': 'computing-science'})
        except:
            resolved_url = ''

        self.assertEqual(resolved_url, '/gubookhub_app/items/computing-science/', "The lookup of URL name didn't return a valid URL matching. Check you have the correct mappings and URL parameters, and try again.")


class ViewTests(TestCase):
    def test_index(self):
        url = reverse('gubookhub_app:index')
        response = self.client.get(url)
        content = response.content.decode()
        self.assertEqual(response.status_code, 200)

        # Checks if correct message appears when no subjects are present
        self.assertIn("There are no subjects present.", content)
        

    def test_about(self):
        url = reverse('gubookhub_app:about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        url = reverse('gubookhub_app:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ImageTests(TestCase):
    def test_header_image(self):
        result = finders.find('images/uofg_header.jpg')
        self.assertIsNotNone(result)

    def test_default_profile_image(self):
        result = finders.find('images/default.jpg')
        self.assertIsNotNone(result)
