from app import create_app
from models import db, Product

app = create_app()

mapping = {
    'Chicken With Skin': '/static/images/products/chicken_skin.svg',
    'Skinless Chicken': '/static/images/products/skinless_chicken.svg',
    'Chicken Liver': '/static/images/products/chicken_liver.svg',
    'Chicken Gizzard': '/static/images/products/chicken_gizzard.svg',
    'Chicken Legs': '/static/images/products/chicken_legs.svg',
    'Chicken Thighs': '/static/images/products/chicken_thighs.svg',
    'Chicken Breast': '/static/images/products/chicken_breast.svg',
    'Chicken Wings': '/static/images/products/chicken_wings.svg',
    'Boneless Chicken': '/static/images/products/boneless_chicken.svg'
}

with app.app_context():
    for name, img_url in mapping.items():
        prod = Product.query.filter_by(name=name).first()
        if prod:
            # If prod doesn't have custom base64 image or if reset needed
            if not prod.image_url or not prod.image_url.startswith('data:'):
                prod.image_url = img_url
                print(f"Updated image URL for {name} -> {img_url}")
    db.session.commit()
    print("Database image mapping sync complete.")
