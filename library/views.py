from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.files import File

import pandas as pd
import os
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from weasyprint import HTML

from .models import Author, Book, Order, Testimonial
from .forms import AuthorForm, BookForm, SignupForm, LoginForm, BuyNowForm
from .utils import send_whatsapp
# views.py
from django.db.models import Count  # add this at the top



# --------- Helper ----------
def admin_required(user):
    return user.is_superuser

# ---------- Author ----------
@login_required
def author_list(request):
    authors = Author.objects.all().order_by('name')
    return render(request, "author_list.html", {"authors": authors})

@login_required
@user_passes_test(admin_required)
def author_create(request):
    form = AuthorForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("author_list")
    return render(request, "author_form.html", {"form": form})

@login_required
@user_passes_test(admin_required)
def author_update(request, pk):
    author = get_object_or_404(Author, pk=pk)
    form = AuthorForm(request.POST or None, instance=author)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("author_list")
    return render(request, "author_form.html", {"form": form})

@login_required
@user_passes_test(admin_required)
def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    author.delete()
    return redirect("author_list")

# ---------- Book ----------
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Book

@login_required
def book_list(request):
    query = request.GET.get('q', '')  # search term
    author_id = request.GET.get('author')  # author filter
    sort_field = request.GET.get('sort', '-published_date')  # sort field, default newest

    # Start with all books
    books = Book.objects.select_related('author').all()

    # Apply search
    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__name__icontains=query)
        )

    # Apply author filter
    if author_id:
        books = books.filter(author_id=author_id)

    # Apply sorting
    books = books.order_by(sort_field)

    # Get all authors for filter dropdown
    authors = Author.objects.all()

    context = {
        "books": books,
        "query": query,
        "authors": authors,
    }
    return render(request, "book_list.html", context)

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "book_detail.html", {"book": book})

@login_required
@user_passes_test(admin_required)
def book_create(request):
    form = BookForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("book_list")
    return render(request, "book_form.html", {"form": form})

@login_required
@user_passes_test(admin_required)
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, request.FILES or None, instance=book)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("book_list")
    return render(request, "book_form.html", {"form": form})

@login_required
@user_passes_test(admin_required)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect("book_list")

# ---------- Like Book ----------
@login_required
def like_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.user in book.likes.all():
        book.likes.remove(request.user)
    else:
        book.likes.add(request.user)
    return redirect('book_list')

# ---------- Auth Views ----------
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
    recent_books = Book.objects.order_by('-id')[:5]
    recent_authors = Author.objects.order_by('-id')[:5]
    testimonials = Testimonial.objects.all()[:3]  # Show 3 testimonials

    # Newsletter form handling
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        email = request.POST.get('newsletter_email')
        # Save email to Newsletter model or send email, as per your logic
        # For demo, just show a message
        messages.success(request, "Thank you for subscribing!")
        return redirect('home')

    return render(request, 'base.html', {
        'recent_books': recent_books,
        'recent_authors': recent_authors,
        'testimonials': testimonials,
    })

# ---------- CSV Upload ----------
@login_required
@user_passes_test(admin_required)
def csvs_upload_books(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]
        print("Uploaded CSV file:", csv_file.name)

        # Try multiple encodings and skip empty lines
        try:
            df = pd.read_csv(csv_file, encoding='utf-8-sig').dropna(how='all')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(csv_file, encoding='ISO-8859-1').dropna(how='all')
            except Exception as e:
                return render(request, "csv_upload.html", {"error": f"Cannot read CSV file: {str(e)}"})
        except pd.errors.EmptyDataError:
            return render(request, "csv_upload.html", {"error": "CSV file has no data."})

        if df.empty:
            return render(request, "csv_upload.html", {"error": "CSV file is empty or has no valid rows."})

        for index, row in df.iterrows():
            # Author
            author_name = row.get('author', 'Unknown Author')
            author, _ = Author.objects.get_or_create(name=author_name)

            # Convert published_date string to date object
            published_date = None
            date_str = row.get('published_date', None)
            if pd.notna(date_str):
                for fmt in ("%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y"):
                    try:
                        published_date = datetime.strptime(str(date_str).strip(), fmt).date()
                        break
                    except ValueError:
                        continue

            # Book instance
            book = Book(
                title=row.get('title', 'Untitled'),
                author=author,
                published_date=published_date,
                price=row.get('price', 0),
                description=row.get('description', '')
            )

            # Image handling
            if 'image' in row and pd.notna(row['image']):
                img_path = row['image']
                img_full_path = os.path.join(settings.BASE_DIR, img_path)
                if os.path.exists(img_full_path):
                    with open(img_full_path, 'rb') as f:
                        book.image.save(os.path.basename(img_path), File(f), save=False)

            book.save()

        return redirect('book_list')

    return render(request, "csv_upload.html")

@csrf_exempt
def api_search_books(request):
    query = request.GET.get("q", "")
    books = Book.objects.filter(
        Q(title__icontains=query) | Q(author__name__icontains=query)
    )

    data = []
    for book in books:
        data.append({
            "id": book.id,
            "title": book.title,
            "author": book.author.name,
            "published_date": book.published_date,
            "price": book.price,
            "description": book.description,
            "image": book.image.url if book.image else None,
        })
    return JsonResponse({"results": data})

# ---------- Order PDF Generation ----------
def _make_order_pdf(order):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # --- Header / Title ---
    p.setFont("Helvetica-Bold", 20)
    p.setFillColor(colors.HexColor("#2C3E50"))
    p.drawCentredString(width / 2, height - 60, "📚 Book Order Summary")

    # Line under heading
    p.setStrokeColor(colors.HexColor("#2980B9"))
    p.setLineWidth(2)
    p.line(50, height - 70, width - 50, height - 70)

    y = height - 110
    p.setFont("Helvetica", 12)
    p.setFillColor(colors.black)

    # Order Info
    order_info = [
        ("Order ID", order.id),
        ("Date", order.created_at.strftime("%d-%m-%Y %H:%M")),
        ("Book", order.book.title),
        ("Author", order.book.author.name),
        ("Price", f"₹{order.book.price}"),
        ("Quantity", order.quantity),
        ("Total", f"₹{order.quantity * order.book.price}"),
    ]

    # Table-style key-value pairs
    for label, value in order_info:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(60, y, f"{label}:")
        p.setFont("Helvetica", 12)
        p.drawString(200, y, str(value))
        y -= 22

    # Buyer Info
    y -= 10
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.HexColor("#34495E"))
    p.drawString(50, y, "Buyer Information")
    y -= 8
    p.setStrokeColor(colors.HexColor("#BDC3C7"))
    p.setLineWidth(1)
    p.line(50, y, width - 50, y)
    y -= 25

    buyer_info = [
        ("Name", order.name),
        ("Email", order.email),
        ("Phone", order.phone),
    ]

    for label, value in buyer_info:
        p.setFont("Helvetica-Bold", 12)
        p.setFillColor(colors.black)
        p.drawString(60, y, f"{label}:")
        p.setFont("Helvetica", 12)
        p.drawString(200, y, str(value))
        y -= 22

    # Address
    y -= 10
    p.setFont("Helvetica-Bold", 12)
    p.drawString(60, y, "Address:")
    y -= 18
    import textwrap
    for line in textwrap.wrap(order.address, width=90):
        p.setFont("Helvetica", 12)
        p.drawString(200, y, line)
        y -= 18

    # Notes (if any)
    if order.notes:
        y -= 15
        p.setFont("Helvetica-Bold", 12)
        p.drawString(60, y, "Notes:")
        y -= 18
        for line in textwrap.wrap(order.notes, width=90):
            p.setFont("Helvetica", 12)
            p.drawString(200, y, line)
            y -= 18

    # Footer
    y = 100
    p.setStrokeColor(colors.HexColor("#95A5A6"))
    p.setLineWidth(0.5)
    p.line(50, y, width - 50, y)

    p.setFont("Helvetica-Oblique", 10)
    p.setFillColor(colors.HexColor("#7F8C8D"))
    p.drawCentredString(width / 2, y - 20, "Thank you for ordering with Library System 📖")

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

# ---------- Buy Now ----------
def buy_now(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        form = BuyNowForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.book = book
            order.save()

            # PDF bytes
            pdf_bytes = _make_order_pdf(order)
            filename = f"order_{order.id}.pdf"

            # --- Admin email ---
            subject_admin = f"New Book Order: {book.title} (#{order.id})"
            body_admin = (
                f"New order received.\n\n"
                f"Order ID: {order.id}\n"
                f"Book: {book.title}\n"
                f"Buyer: {order.name}\n"
                f"Email: {order.email}\n"
                f"Phone: {order.phone}\n"
                f"Qty: {order.quantity}\n"
            )
            email_admin = EmailMessage(
                subject_admin,
                body_admin,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ORDER_NOTIFICATION_EMAIL],
            )
            email_admin.attach(filename, pdf_bytes, "application/pdf")
            email_admin.send(fail_silently=False)

            # --- User email ---
            subject_user = "Your Book Order Confirmation"
            body_user = (
                f"Hi {order.name},\n\n"
                f"Thanks for your order of '{book.title}'. "
                "We've attached your order summary as PDF.\n\n"
                "We'll contact you soon with shipping details.\n\n"
                "Regards,\nLibrary Team"
            )
            email_user = EmailMessage(
                subject_user,
                body_user,
                settings.DEFAULT_FROM_EMAIL,
                [order.email],
            )
            email_user.attach(filename, pdf_bytes, "application/pdf")
            email_user.send(fail_silently=True)

            messages.success(request, "Order placed! Confirmation email sent.")
            return redirect("book_list")
    else:
        form = BuyNowForm()

    return render(request, "buy_now.html", {"form": form, "book": book})

def order_pdf_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # ✅ Render HTML inside the function
    html_string = render_to_string('library/order_pdf.html', {'order': order})

    # Generate PDF
    pdf_file = HTML(string=html_string).write_pdf()

    # Send PDF via email
    email = EmailMessage(
        subject=f"Your Order #{order.id}",
        body="Please find your order attached.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[order.email],
    )
    email.attach(f'order_{order.id}.pdf', pdf_file, 'application/pdf')
    email.send()

    # Return PDF as download
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_{order.id}.pdf"'
    return response

def send_order_pdf_email(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Render HTML template
    html = render_to_string('library/order_pdf.html', {'order': order})
    pdf_file = HTML(string=html).write_pdf()

    # Send email with PDF attachment
    email = EmailMessage(
        subject=f"Your Order #{order.id}",
        body="Please find your order PDF attached.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[order.email],
    )
    email.attach(f'order_{order.id}.pdf', pdf_file, 'application/pdf')
    email.send()
    
    messages.success(request, "Order confirmation email sent!")
    return redirect('book_list')


from .utils import send_whatsapp
from django.core.mail import EmailMessage
from django.contrib import messages

def buy_now(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        form = BuyNowForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.book = book
            order.save()

            # Generate PDF
            pdf_bytes = _make_order_pdf(order)
            filename = f"order_{order.id}.pdf"

            # --- Send Email ---
            email_user = EmailMessage(
                subject=f"Order Confirmation #{order.id}",
                body=f"Hi {order.name}, your order is confirmed. PDF attached.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[order.email]
            )
            email_user.attach(filename, pdf_bytes, 'application/pdf')
            email_user.send(fail_silently=True)

            # --- Send WhatsApp ---
            send_whatsapp(order, pdf_bytes)

            messages.success(request, "Order placed! Email & WhatsApp notification sent.")
            return redirect("book_list")
    else:
        form = BuyNowForm()

    return render(request, "buy_now.html", {"form": form, "book": book})

# library/views.py
from django.http import JsonResponse
from django.contrib.auth.models import User   # ✅ ye add karo
from .models import Book, Author



def counters(request):
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    data = {
        "total_books": total_books,
        "total_authors": total_authors,
        "active_users": active_users,

        
    }
    return JsonResponse(data)

from .forms import ContactForm

def contact_submit(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save data to DB
            return JsonResponse({"status": "success", "message": "Message sent successfully!"})
        else:
            return JsonResponse({"status": "error", "message": "Invalid form data!"})
    return JsonResponse({"status": "error", "message": "Invalid request!"})


from django.contrib import messages
from .models import NewsletterSubscriber

def subscribe_newsletter(request):
    if request.method == "POST":
        email = request.POST.get("newsletter_email")
        if email:
            # check if already subscribed
            if NewsletterSubscriber.objects.filter(email=email).exists():
                messages.warning(request, "You are already subscribed!")
            else:
                NewsletterSubscriber.objects.create(email=email)
                messages.success(request, "Thank you for subscribing!")
        else:
            messages.error(request, "Please enter a valid email.")
        return redirect("home")  # apna homepage ya jis page par ho use redirect karo

from .models import Book, Author

def recent_books_and_authors(request):
    recent_books = Book.objects.order_by('-id')[:5]  # last 5 books
    recent_authors = Author.objects.order_by('-id')[:5]  # last 5 authors
    return {
        'recent_books': recent_books,
        'recent_authors': recent_authors,
    }

login_required
def profile_view(request):
    return render(request, "profile.html")

@login_required
def settings_view(request):
    return render(request, "settings.html")


# views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile

@login_required
def settings_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your account has been updated!")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'settings.html', context)


from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # login session update karne ke liye
            messages.success(request, '✅ Password changed successfully!')
            return redirect('profile')  # profile page pe redirect
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})

def dashboard(request):
    return render(request, "dashboard.html")



# Top Authors API
def api_top_authors(request):
    data = Book.objects.values("author__name").annotate(count=Count("id")).order_by("-count")[:8]
    labels = [d["author__name"] for d in data]
    counts = [d["count"] for d in data]
    return JsonResponse({"labels": labels, "counts": counts})

# Books by Genre API ✅
def api_books_by_genre(request):
    # Agar genre CharField hai
    data = Book.objects.values("genre").annotate(count=Count("id")).order_by("-count")
    labels = [d["genre"] for d in data]
    counts = [d["count"] for d in data]
    return JsonResponse({"labels": labels, "counts": counts})

# Agar genre ForeignKey hai:
# data = Book.objects.values("genre__name").annotate(count=Count("id")).order_by("-count")
# labels = [d["genre__name"] for d in data]
