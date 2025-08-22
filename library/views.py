from django.shortcuts import render, redirect, get_object_or_404
from .models import Author, Book
from .forms import AuthorForm, BookForm

# ---------- Author ----------
def author_list(request):
    authors = Author.objects.all().order_by('name')
    return render(request, "author_list.html", {"authors": authors})

def author_create(request):
    form = AuthorForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("author_list")
    return render(request, "author_form.html", {"form": form})

def author_update(request, pk):
    author = get_object_or_404(Author, pk=pk)
    form = AuthorForm(request.POST or None, instance=author)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("author_list")
    return render(request, "author_form.html", {"form": form})

def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    author.delete()
    return redirect("author_list")

# ---------- Book ----------
def book_list(request):
    books = Book.objects.select_related('author').all().order_by('-published_date')
    return render(request, "book_list.html", {"books": books})

def book_create(request):
    form = BookForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("book_list")
    return render(request, "book_form.html", {"form": form})

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("book_list")
    return render(request, "book_form.html", {"form": form})

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect("book_list")

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "library/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = LoginForm()
    return render(request, "library/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def home(request):
    return render(request, "library/home.html")

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book

@login_required
def like_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.user in book.likes.all():
        book.likes.remove(request.user)  # Unlike
    else:
        book.likes.add(request.user)  # Like
    return redirect('book_list')
from django.shortcuts import render, redirect
from .forms import BookForm

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)  # <-- Important
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form})
