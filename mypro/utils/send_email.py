# library/utils/send_email.py
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_order_email(order):
    """
    Send order confirmation email with proper error handling.
    Will not crash if email sending fails.
    """
    try:
        subject = f"Order Confirmation #{order.id}"
        message = f"Hello {order.name},\n\nThank you for your order of {order.book.title}."
        recipient_list = [order.email]
        
        # Send email with fail_silently=True to prevent blocking
        send_mail(
            subject, 
            message, 
            settings.DEFAULT_FROM_EMAIL, 
            recipient_list,
            fail_silently=True  # Critical: Don't raise exceptions
        )
        
        logger.info(f"✅ Order confirmation email sent successfully for Order #{order.id}")
        
    except Exception as e:
        # Log the error but don't crash the order creation
        logger.error(f"❌ Failed to send order confirmation email for Order #{order.id}: {str(e)}")
        # Return gracefully - order should still be saved
        pass
