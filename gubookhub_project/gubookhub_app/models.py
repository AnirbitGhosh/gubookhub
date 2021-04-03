from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subject, self).save(*args, **kwargs)
    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=128, unique=True)
    level = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Book(models.Model):
    TITLE_MAX_LENGTH = 128
    AUTHOR_MAX_LENGTH = 128
    URL_MAX_LENGTH = 256

    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    author = models.CharField(max_length=128)
    url = models.URLField(max_length=256, null=True, blank=True)
    favorite_count = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    level = models.IntegerField(blank=False)
    subject = models.CharField(max_length=128, blank=False) # Considering making it a foreign key later on
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

class Favorite(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # User favorited: Book
        return self.book + ' favorited by: ' + self.user.name
