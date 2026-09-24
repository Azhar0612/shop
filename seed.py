import os
from app import create_app
from models import db, Admin, Product, Setting, Review

app = create_app()

def seed_database():
    with app.app_context():
        db.create_all()

        # Seed or sync Admin user from environment settings
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin(username='admin')
            db.session.add(admin)

        env_admin_pass = os.environ.get('ADMIN_PASSWORD')
        if env_admin_pass:
            admin.set_password(env_admin_pass)
        elif not admin.password_hash:
            admin.set_password('dev-admin-pass')
        print("Admin user synchronization complete.")

        # Initial products list as defined in specification
        initial_products = [
            {
                'name': 'Chicken With Skin',
                'category': 'Fresh Chicken',
                'price_per_kg': 240.0,
                'description': 'Fresh chicken with skin intact. Farm fresh, hygienic, sourced from Sneha Fresh Chicken.',
                'image_url': '/static/images/products/chicken_skin.svg',
                'is_available': True
            },
            {
                'name': 'Skinless Chicken',
                'category': 'Fresh Chicken',
                'price_per_kg': 260.0,
                'description': 'Tender, skinless fresh chicken cuts prepared hygienically on order.',
                'image_url': '/static/images/products/skinless_chicken.svg',
                'is_available': True
            },
            {
                'name': 'Chicken Liver',
                'category': 'Chicken Organs',
                'price_per_kg': 160.0,
                'description': 'Fresh, nutrient-rich chicken liver cleaned carefully for your recipes.',
                'image_url': '/static/images/products/chicken_liver.svg',
                'is_available': True
            },
            {
                'name': 'Chicken Gizzard',
                'category': 'Chicken Organs',
                'price_per_kg': 160.0,
                'description': 'Fresh cleaned chicken gizzard ready for spicy curries and fry dishes.',
                'image_url': '/static/images/products/chicken_gizzard.svg',
                'is_available': True
            },
            {
                'name': 'Chicken Legs',
                'category': 'Special Cuts',
                'price_per_kg': 360.0,
                'description': 'Juicy drumsticks & full chicken legs ideal for tandoori, fry, or biryani.',
                'image_url': '/static/images/products/chicken_legs.svg',
                'is_available': True
            },
            {
                'name': 'Chicken Thighs',
                'category': 'Special Cuts',
                'price_per_kg': 340.0,
                'description': 'Flavorful chicken thighs cut according to your culinary preference.',
                'image_url': '/static/images/products/chicken_thighs.svg',
                'is_available': True
            },
            {
                'name': 'Chicken Breast',
                'category': 'Special Cuts',
                'price_per_kg': 300.0,
                'description': 'Lean, protein-packed fresh chicken breast cut to your exact requirements.',
                'image_url': '/static/images/products/chicken_breast.svg',
                'is_available': True
            },
            {
                'name': 'Chicken Wings',
                'category': 'Special Cuts',
                'price_per_kg': 400.0,
                'description': 'Tender fresh chicken wings perfect for roasting, grilling, or frying.',
                'image_url': '/static/images/products/chicken_wings.svg',
                'is_available': True
            },
            {
                'name': 'Boneless Chicken',
                'category': 'Special Cuts',
                'price_per_kg': 500.0,
                'description': '100% pure boneless chicken meat, ideal for chicken 65, kebabs, and curries.',
                'image_url': '/static/images/products/boneless_chicken.svg',
                'is_available': True
            }
        ]

        for prod in initial_products:
            existing = Product.query.filter_by(name=prod['name']).first()
            if not existing:
                p = Product(**prod)
                db.session.add(p)
                print(f"Added product: {prod['name']} at Rs.{prod['price_per_kg']}/kg")
            else:
                print(f"Product already exists: {prod['name']}")

        # Initial Website Settings
        settings_data = [
            ('shop_name', 'Jahangeer Chicken Center', 'Business Name'),
            ('supplier_brand', 'Sneha Fresh Chicken', 'Chicken Supplier Brand'),
            ('phone_primary', '9908014554', 'Primary Contact Phone'),
            ('phone_secondary', '6302113176', 'Alternate Contact Phone'),
            ('whatsapp_number', '9908014554', 'WhatsApp Business Number'),
            ('address_line', 'Jahangir Chicken Center, Opposite Army College of Dental Sciences, Rajiv Swagruha ABHIMAAN Project, Secunderabad, Telangana - 500087', 'Shop Physical Address'),
            ('opening_hours', 'Every day 7:00 AM - 10:00 PM', 'Daily Store Hours'),
            ('maps_url', 'https://maps.app.goo.gl/sj876gsP9mo6CVot5?g_st=ac', 'Google Maps Location Link'),
            ('instagram_url', 'https://www.instagram.com/md7400306?stkn=MTBsZDhxaWxtYzBjdg==', 'Instagram Profile Link'),
            ('facebook_url', '', 'Facebook Page Link (Configurable)')
        ]

        for key, val, desc in settings_data:
            setting_obj = Setting.query.filter_by(key=key).first()
            if not setting_obj:
                db.session.add(Setting(key=key, value=val, description=desc))

        db.session.commit()
        print("Database seed completed successfully.")

if __name__ == '__main__':
    seed_database()
