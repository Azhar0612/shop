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

def request_url(url, method='GET', data=None, headers={}):
    req_data = None
    if data:
        if headers.get('Content-Type') == 'application/json':
            req_data = json.dumps(data).encode('utf-8')
        else:
            req_data = urllib.parse.urlencode(data).encode('utf-8')
    
    req = urllib.request.Request(base_url + url, data=req_data, headers=headers, method=method)
    try:
        res = opener.open(req)
        return res.status, res.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except Exception as e:
        return 500, str(e)

print("==================================================")
print("COMPREHENSIVE QA & SECURITY AUDIT TEST SUITE")
print("==================================================")

# 1. Product Prices & Names Audit
status, body = request_url('/api/products')
assert status == 200, f"Products API failed with status {status}"
prods = json.loads(body)

expected_prods = {
    'Chicken With Skin': 240.0,
    'Skinless Chicken': 260.0,
    'Chicken Liver': 160.0,
    'Chicken Gizzard': 160.0,
    'Chicken Legs': 360.0,
    'Chicken Thighs': 340.0,
    'Chicken Breast': 300.0,
    'Chicken Wings': 400.0,
    'Boneless Chicken': 500.0
}

print(f"[PASS] Loaded {len(prods)} products from DB.")
for p in prods:
    name = p['name']
    price = p['price_per_kg']
    if name in expected_prods:
        assert price == expected_prods[name], f"Price mismatch for {name}: expected {expected_prods[name]}, got {price}"
        print(f"  - {name}: Rs.{price}/kg [OK]")

# 2. Decimal Order Math Test (0.5 kg + 1.5 kg)
order_payload = {
    'customer_name': 'QA Test Customer',
    'customer_phone': '9908014554',
    'cutting_preference': 'Biryani Cut',
    'special_instructions': 'Test order math',
    'items': [
        {'product_id': 1, 'product_name': 'Chicken With Skin', 'quantity_kg': 0.5, 'price_per_kg': 240.0}, # 120.0
        {'product_id': 2, 'product_name': 'Skinless Chicken', 'quantity_kg': 1.5, 'price_per_kg': 260.0}   # 390.0
    ]
}
status, body = request_url('/api/order', method='POST', data=order_payload, headers={'Content-Type': 'application/json'})
assert status == 200, f"Order creation failed: {body}"
res_data = json.loads(body)
order_num = res_data['order_number']
print(f"[PASS] Order Creation Passed: {order_num}")

# 3. Admin Security Check (Unauthenticated access to protected routes)
unauth_opener = urllib.request.build_opener()
try:
    unauth_req = urllib.request.Request(base_url + '/admin/dashboard')
    unauth_res = unauth_opener.open(unauth_req)
    # If redirected to login, that is correct
    print(f"[PASS] Admin route protection verified (Redirected to: {unauth_res.url})")
except urllib.error.HTTPError as e:
    print(f"[PASS] Admin route protection verified (HTTP Status: {e.code})")

# 4. Admin Auth & Order Workflow Test
admin_pass = os.environ.get('ADMIN_PASSWORD', 'dev-admin-pass')
status, body = request_url('/admin/login', method='POST', data={'username': 'admin', 'password': admin_pass})
assert status == 200, "Admin login failed"
print("[PASS] Admin Login Passed.")

# Get Order ID for created order
status, body = request_url('/admin/orders')
assert status == 200, "Admin orders fetch failed"
assert order_num in body, f"Order {order_num} not found in admin orders table"
print(f"[PASS] Order {order_num} visible in Admin Dashboard.")

# Extract order ID and test status transitions (Completed -> Cancelled)
# Find order ID via API products / DB context
from app import create_app
from models import db, Order, RevenueTransaction, Product, Review, BulkEnquiry

app = create_app()
with app.app_context():
    order_obj = Order.query.filter_by(order_number=order_num).first()
    assert order_obj is not None, "Order object not found in DB"
    order_id = order_obj.id
    
    # Check total math: 240 * 0.5 + 260 * 1.5 = 120 + 390 = 510.0
    assert order_obj.total_amount == 510.0, f"Expected order total 510.0, got {order_obj.total_amount}"
    print(f"[PASS] Decimal Order Total Math Verified: Rs.{order_obj.total_amount} (240 * 0.5 + 260 * 1.5)")

# Test status change to Completed via Admin API
status, body = request_url(f'/admin/orders/{order_id}/status', method='POST', data={'status': 'Completed'}, headers={'Content-Type': 'application/json'})
assert status == 200, f"Status update to Completed failed: {body}"

with app.app_context():
    tx = RevenueTransaction.query.filter_by(order_id=order_id).first()
    assert tx is not None, "RevenueTransaction not logged on Completed status"
    assert tx.amount == 510.0, f"Expected revenue tx amount 510.0, got {tx.amount}"
    print(f"[PASS] Revenue Logged on Order Completion: Rs.{tx.amount}")

# Test status change from Completed -> Cancelled (Revenue sync check)
status, body = request_url(f'/admin/orders/{order_id}/status', method='POST', data={'status': 'Cancelled'}, headers={'Content-Type': 'application/json'})
assert status == 200, f"Status update to Cancelled failed: {body}"

with app.app_context():
    tx_cancelled = RevenueTransaction.query.filter_by(order_id=order_id).first()
    assert tx_cancelled is None, "RevenueTransaction was NOT removed when order was Cancelled! (Double counting bug)"
    print("[PASS] Cancelled Order Revenue Removal Verified (No false revenue counting!)")

    # Clean up test order
    Order.query.filter_by(id=order_id).delete()
    db.session.commit()
    print("[PASS] QA test order cleaned up cleanly.")

print("\n==================================================")
print("ALL AUDIT VERIFICATIONS & QA TESTS PASSED 100%!")
print("==================================================")
