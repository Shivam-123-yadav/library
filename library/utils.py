# utils.py
from twilio.rest import Client
from django.conf import settings

def send_whatsapp(order, pdf_bytes):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    to_number = f"whatsapp:+91{order.phone[-10:]}"
    from_number = settings.TWILIO_WHATSAPP_FROM

    # Order ki sari info message me
    message_body = (
        f"Order Confirmed!\n"
        f"Order ID: {order.id}\n"
        f"Book: {order.book.title}\n"
        f"Customer: {order.name}\n"  # <-- yahan .name use karein
        f"Phone: {order.phone}\n"
        f"Address: {order.address}\n"
        f"Thank you for your order!"
    )

    client.messages.create(
        body=message_body,
        from_=from_number,
        to=to_number
    )
