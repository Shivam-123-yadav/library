# library/utils/send_email.py
from django.core.mail import send_mail
from django.conf import settings

def send_order_email(order):
    subject = f"Order Confirmation #{order.id}"
    message = f"Hello {order.name},\n\nThank you for your order of {order.book.title}."
    recipient_list = [order.email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
