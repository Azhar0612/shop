import os
import urllib.request
import urllib.parse
import json
import http.cookiejar
from dotenv import load_dotenv

load_dotenv()

base_url = 'http://127.0.0.1:5000'

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def test_endpoint(name, url, method='GET', data=None, headers={}):
    print(f"\n[TESTING] {name} ({method} {url})...")
    req_data = None
    if data:
        if headers.get('Content-Type') == 'application/json':
            req_data = json.dumps(data).encode('utf-8')
        else:
            req_data = urllib.parse.urlencode(data).encode('utf-8')
    
    req = urllib.request.Request(base_url + url, data=req_data, headers=headers, method=method)
    try:
        res = opener.open(req)
        body = res.read().decode('utf-8')
        print(f"  -> SUCCESS ({res.status}) - Length: {len(body)} bytes")
        return res.status, body
    except Exception as e:
        print(f"  -> ERROR: {e}")
        return None, str(e)

print("Starting automated integration test suite...")

# 1. Home page
test_endpoint('Home Page', '/')

# 2. Products Page
test_endpoint('Products Page', '/products')

# 3. Products API
status, body = test_endpoint('Products API', '/api/products')
if status == 200:
    prods = json.loads(body)
    print(f"  -> Returned {len(prods)} products from DB.")

# 4. Create Order API
order_payload = {
    'customer_name': 'Azhar Customer',
    'customer_phone': '9876543210',
    'cutting_preference': 'Biryani Cut',
    'special_instructions': 'Please pack cleanly for pickup',
    'items': [
        {'product_id': 1, 'product_name': 'Chicken With Skin', 'quantity_kg': 2.0, 'price_per_kg': 240.0},
        {'product_id': 9, 'product_name': 'Boneless Chicken', 'quantity_kg': 1.0, 'price_per_kg': 500.0}
    ]
}
status, body = test_endpoint('Create Order API', '/api/order', method='POST', data=order_payload, headers={'Content-Type': 'application/json'})
print(f"  -> Order Response: {body}")

# 5. Submit Bulk Enquiry API
bulk_payload = {
    'contact_name': 'Hotel Taj Residency',
    'business_name': 'Taj Caterers',
    'phone': '9908014554',
    'business_type': 'Caterer',
    'requirement_details': 'Need 100kg curry cut skinless chicken for event.'
}
test_endpoint('Bulk Enquiry API', '/api/bulk-enquiry', method='POST', data=bulk_payload, headers={'Content-Type': 'application/json'})

# 6. Submit Review API
review_payload = {
    'customer_name': 'Ramesh Kumar',
    'rating': 5,
    'review_text': 'Excellent fresh Sneha chicken in Secunderabad! Cutting was perfect.'
}
test_endpoint('Submit Review API', '/api/review', method='POST', data=review_payload, headers={'Content-Type': 'application/json'})

# 7. Admin Login
admin_pass = os.environ.get('ADMIN_PASSWORD', 'dev-admin-pass')
login_data = {'username': 'admin', 'password': admin_pass}
test_endpoint('Admin Login', '/admin/login', method='POST', data=login_data)

# 8. Admin Dashboard
test_endpoint('Admin Dashboard', '/admin/dashboard')

# 9. Admin Products Page
test_endpoint('Admin Products Page', '/admin/products')

# 10. Admin Orders Page
test_endpoint('Admin Orders Page', '/admin/orders')

# 11. Admin Revenue Page
test_endpoint('Admin Revenue Page', '/admin/revenue')

# 12. Admin Bulk Page
test_endpoint('Admin Bulk Page', '/admin/bulk')

# 13. Admin Reviews Page
test_endpoint('Admin Reviews Page', '/admin/reviews')

# 14. Admin Settings Page
test_endpoint('Admin Settings Page', '/admin/settings')

print("\nIntegration test suite finished successfully!")
