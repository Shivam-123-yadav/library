from django.urls import path
from . import views

from twilio.rest import Client
from django.conf import settings

def send_whatsapp(order, pdf_bytes):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Save PDF temporarily
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f.write(pdf_bytes)
        f_path = f.name

    # Twilio Sandbox supports media as URL, so for local dev use ngrok or send text only
    # Here we send a simple text notification
    client.messages.create(
        from_=settings.TWILIO_WHATSAPP_FROM,
        to=f"whatsapp:{order.phone}",  # Make sure number has +91
        body=f"Hi {order.name}, your order #{order.id} for '{order.book.title}' is confirmed!"
    )

    # Optional: remove temp file
    import os
    os.remove(f_path)


urlpatterns = [
    # Authors
    path("authors/", views.author_list, name="author_list"),
    path("authors/add/", views.author_create, name="author_create"),
    path("authors/<int:pk>/edit/", views.author_update, name="author_update"),
    path("authors/<int:pk>/delete/", views.author_delete, name="author_delete"),
    path("buy_now/<int:pk>/", views.buy_now, name="buy_now"),
    path('order/<int:order_id>/pdf/', views.send_order_pdf_email, name='order_pdf'),
    path('order/<int:order_id>/pdf/', views.order_pdf_view, name='order_pdf'),
    path('change-password/', views.change_password_view, name='change_password'),
     path('api/books-by-genre/', views.api_books_by_genre, name='api_books_by_genre'),  # ✅ important
     path("authors/<int:author_id>/books/", views.books_by_author, name="books_by_author"),
    #  path("test-pdf/", views.test_pdf, name="test_pdf"),

    # Books
    path("book_list/", views.book_list, name="book_list"),
    path("books/add/", views.book_create, name="book_create"),
    path("books/<int:pk>/edit/", views.book_update, name="book_update"),
    path("books/<int:pk>/delete/", views.book_delete, name="book_delete"),
    path("books/<int:book_id>/like/", views.like_book, name="like_book"),
    path("book/<int:pk>/", views.book_detail, name="book_detail"),
    path('books/csv_upload/', views.csvs_upload_books, name='csvs_upload_books'),
    path("books/search_api/", views.api_search_books, name="api_search_books"),
    path("books/search/", views.book_list, name="book_search"),
    path("counters/", views.counters, name="counters"),
    path("contact-submit/", views.contact_submit, name="contact_submit"),
    path("subscribe/", views.subscribe_newsletter, name="subscribe_newsletter"),
    path("profile/", views.profile_view, name="profile"),
    path("settings/", views.settings_view, name="settings"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("api/top-authors/", views.api_top_authors, name="api_top_authors"),
]
