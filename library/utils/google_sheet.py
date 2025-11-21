import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_path = "library/utils/credentials.json"
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)

    sheet_id = "1yINKvqlLRjSM5R0_VMuZ9jYaCxYNc9XVgHFWFEyVXs4"
    sheet = client.open_by_key(sheet_id).sheet1
    return sheet


def save_to_google_sheet(order):
    """Push single order to Google Sheet."""
    sheet = get_sheet()

    row = [
        order.id,
        order.book.title if order.book else "",
        order.name,
        order.email,
        order.phone,
        order.address,
        order.quantity,
        order.notes,
        order.status,
        str(order.created_at)
    ]
    sheet.append_row(row)


def push_all_orders_to_sheet():
    """Push all orders from DB to Google Sheet (with headings)."""
    # Import Order **inside function** to avoid circular import
    from library.models import Order

    sheet = get_sheet()
    sheet.clear()  # optional, purane incorrect data clear karne ke liye

    headers = [
        "ID", "Book Title", "Name", "Email", "Phone",
        "Address", "Quantity", "Notes", "Status", "Created At"
    ]
    sheet.append_row(headers)

    orders = Order.objects.all()
    for order in orders:
        save_to_google_sheet(order)

    print(f"✅ Total {orders.count()} orders added to Google Sheet.")

