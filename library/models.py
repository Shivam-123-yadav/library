# library/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save   # ✅ post_save ke liye
from django.dispatch import receiver             # ✅ receiver ke liye
from .utils.google_sheet import save_to_google_sheet
from .utils import send_whatsapp, send_order_email





class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True) 
    published_date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    likes = models.ManyToManyField(User, related_name="liked_books", blank=True)
    def total_likes(self):
        return self.likes.count()
    def __str__(self):
        return self.title

# ✅ NEW
class Order(models.Model):
    STATUS_CHOICES = (
        # ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='orders')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

# ✅ Signal: jab new Order create hoga to Google Sheet me add ho
# Signal to send data to Google Sheet, WhatsApp, and Email after order is created
@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    if created:
        try:
            save_to_google_sheet(instance)
            print("✅ Order added to Google Sheet")
        except Exception as e:
            print("⚠️ Google Sheet Error:", e)

        try:
            send_whatsapp(instance)
            print("✅ WhatsApp message sent")
        except Exception as e:
            print("⚠️ WhatsApp Error:", e)

        try:
            send_order_email(instance)
            print("✅ Email sent")
        except Exception as e:
            print("⚠️ Email Error:", e)
class Testimonial(models.Model):
    user_name = models.CharField(max_length=100)
    content = models.TextField()

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')



    def __str__(self):
        return f"Order #{self.id} - {self.book.title}"
