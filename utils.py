import os
import urllib.parse
from functools import wraps
from flask import session, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from models import Setting

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in to access the admin dashboard.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def get_site_settings():
    settings_records = Setting.query.all()
    settings_dict = {}
    for s in settings_records:
        settings_dict[s.key] = s.value
    
    # Defaults if not in DB
    defaults = {
        'shop_name': 'Jahangeer Chicken Center',
        'supplier_brand': 'Sneha Fresh Chicken',
        'phone_primary': '9908014554',
        'phone_secondary': '6302113176',
        'whatsapp_number': '9908014554',
        'address_line': 'Jahangir Chicken Center, Opposite Army College of Dental Sciences, Rajiv Swagruha ABHIMAAN Project, Secunderabad, Telangana - 500087',
        'opening_hours': 'Every day 7:00 AM - 10:00 PM',
        'maps_url': 'https://maps.app.goo.gl/sj876gsP9mo6CVot5?g_st=ac',
        'instagram_url': 'https://www.instagram.com/md7400306?stkn=MTBsZDhxaWxtYzBjdg==',
        'facebook_url': ''
    }
    for k, v in defaults.items():
        if k not in settings_dict:
            settings_dict[k] = v
    return settings_dict

def generate_whatsapp_order_link(phone, customer_name, items_list, cutting_preference, special_instructions):
    clean_phone = ''.join(filter(str.isdigit, phone))
    if not clean_phone.startswith('91') and len(clean_phone) == 10:
        clean_phone = '91' + clean_phone

    msg_lines = [
        "Hello Jahangeer Chicken Center,",
        "",
        f"Name: {customer_name}",
        "I would like to order:",
    ]
    for item in items_list:
        msg_lines.append(f"• {item['name']} - {item['quantity_kg']} kg")

    msg_lines.append("")
    msg_lines.append(f"Cutting preference:\n{cutting_preference}")
    if special_instructions:
        msg_lines.append(f"\nSpecial instructions:\n{special_instructions}")
    
    msg_lines.append("\nI will pick it up from the shop.")
    msg_lines.append("\nThank you.")

    full_message = "\n".join(msg_lines)
    encoded_message = urllib.parse.quote(full_message)
    return f"https://wa.me/{clean_phone}?text={encoded_message}"
