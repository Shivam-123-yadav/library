# library/utils/pdf.py
from io import BytesIO
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile

def _make_order_pdf(order):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, f"Order ID: {order.id}")
    c.drawString(100, 730, f"Name: {order.name}")
    c.drawString(100, 710, f"Book: {order.book.title if order.book else ''}")
    c.drawString(100, 690, f"Quantity: {order.quantity}")
    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

def generate_and_save_pdf(order):
    pdf_bytes = _make_order_pdf(order)
    filename = f"order_{order.id}.pdf"
    # Agar aapko media folder me save karna hai:
    from django.core.files.storage import default_storage
    path = f"whatsapp_orders/{filename}"
    default_storage.save(path, ContentFile(pdf_bytes))
    # Return a URL (for example, using django's default storage url)
    return default_storage.url(path)
