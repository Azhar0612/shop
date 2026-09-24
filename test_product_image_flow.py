import urllib.request
import urllib.parse
import json
import http.cookiejar
import base64

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
        return res.status, res.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return 500, str(e).encode('utf-8')

print("==================================================")
print("PRODUCT IMAGE FLOW & RENDER VERIFICATION SUITE")
print("==================================================")

# 1. Fetch public API products and verify image URLs
status, body = request_url('/api/products')
assert status == 200, f"Products API failed with status {status}"
prods = json.loads(body.decode('utf-8'))

print(f"[PASS] Loaded {len(prods)} products from API.")

for p in prods:
    name = p['name']
    img_url = p['image_url']
    assert img_url and len(img_url) > 0, f"Missing image URL for product: {name}"
    
    if img_url.startswith('data:'):
        print(f"  - {name}: Base64 Data URL ({len(img_url)} chars) [OK]")
    else:
        # Static asset URL check
        img_status, img_body = request_url(img_url)
        assert img_status == 200, f"Failed to fetch static image {img_url} for {name} (HTTP {img_status})"
        assert len(img_body) > 100, f"Image {img_url} for {name} is surprisingly small ({len(img_body)} bytes)"
        print(f"  - {name}: Static Asset {img_url} ({len(img_body)} bytes) [OK]")

# 2. Base64 Image DB & Rendering Test
from app import create_app
from models import db, Product

app = create_app()
sample_png_b64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="

with app.app_context():
    prod = Product.query.filter_by(name='Chicken With Skin').first()
    original_url = prod.image_url
    
    # Test setting custom Base64 image
    prod.image_url = sample_png_b64
    db.session.commit()
    print("[PASS] Updated product 'Chicken With Skin' image_url in DB to Base64 string.")

# Verify public API returns updated image URL
status, body = request_url('/api/products')
prods_updated = json.loads(body.decode('utf-8'))
prod_skin = next(p for p in prods_updated if p['name'] == 'Chicken With Skin')
assert prod_skin['image_url'] == sample_png_b64, "Public API did not return updated Base64 image_url!"
print("[PASS] Public API dynamically returned updated Base64 image string.")

# Verify HTML page renders updated image URL
status, html = request_url('/products')
html_str = html.decode('utf-8')
assert 'data:image/png;base64,' in html_str, "Public /products HTML did not render updated Base64 image string!"
print("[PASS] Public /products HTML rendered updated image URL.")

# Restore original image URL
with app.app_context():
    prod = Product.query.filter_by(name='Chicken With Skin').first()
    prod.image_url = original_url
    db.session.commit()
    print("[PASS] Restored original product image URL.")

print("\n==================================================")
print("PRODUCT IMAGE FLOW VERIFIED 100% SUCCESSFUL!")
print("==================================================")
