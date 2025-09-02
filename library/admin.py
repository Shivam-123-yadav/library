from django.contrib import admin

from library.models import Author, Book

admin.site.register(Author)
admin.site.register(Book)

# Register your models here.
# library/admin.py
from django.contrib import admin
from .models import Author, Book, Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "name", "quantity", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "phone", "book__title")
