from django.contrib import admin
from gubookhub_app.models import Profile
from gubookhub_app.models import Subject, Course, Book

# Register your models here.
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Book)
admin.site.register(Profile)