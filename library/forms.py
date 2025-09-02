from django import forms
from .models import Author, Book

from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author','description','published_date', 'price', 'image']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'})
        }
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

# Signup form (custom)
class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# Login form (custom)
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

from django import forms
from .models import Order

# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ["name", "email", "phone", "address", "quantity"]


# library/forms.py

class BuyNowForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "email", "phone", "address", "quantity", "notes"]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'mobile', 'bio', 'avatar']
