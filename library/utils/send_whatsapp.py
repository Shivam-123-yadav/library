def send_whatsapp(order, pdf_url=None):
    # yaha Twilio ya kisi aur API ka code use karo
    phone = order.phone
    message = f"Hello {order.name}, your order #{order.id} has been received."
    if pdf_url:
        message += f" PDF: {pdf_url}"
    
    # Example: print instead of sending for now
    print(f"WhatsApp message to {phone}: {message}")
