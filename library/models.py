from django.db import models
from django.contrib.auth.models import User
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    published_date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.title
    
    likes = models.ManyToManyField(User, related_name="liked_books", blank=True)
    
    def total_likes(self):
        return self.likes.count()
