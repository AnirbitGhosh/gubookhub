from django import template
from gubookhub_app.models import Course, Subject, Book
from gubookhub_app.helpers import list_split

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.inclusion_tag('gubookhub/courses.html')
def get_courses_list(subject_name):
    subject = Subject.objects.get(name=subject_name)

    courses = Course.objects.filter(subject=subject).order_by('title')
    context = {}
    context['courses'] = courses
    number_of_books = {}
    for course in courses:
        number_of_books[course] = len(Book.objects.filter(course=course))
    context['number_of_books'] = number_of_books
    return context

@register.inclusion_tag('gubookhub/subjects_list.html')
def get_subjects_list(current_subject=None):
    return {'subjects' : Subject.objects.all(), 'current_subject':current_subject}

@register.inclusion_tag('gubookhub/subjects_card.html')
def get_subjects_cards():
    return {'subjects_output' : list_split(Subject.objects.all(),6)}

