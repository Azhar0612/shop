import os
import tempfile
import uuid
import base64
import urllib.parse
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from config import Config
from models import db, Admin, Product, Order, OrderItem, Review, BulkEnquiry, RevenueTransaction, Setting
from utils import admin_required, allowed_file, get_site_settings, generate_whatsapp_order_link

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Safely create upload folder with fallback for read-only serverless filesystems
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except (OSError, PermissionError):
        app.config['UPLOAD_FOLDER'] = os.path.join(tempfile.gettempdir(), 'uploads')
        try:
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        except Exception:
            pass

    # Automatic DB Initialization & Seeder on Startup for Serverless (Vercel)
    with app.app_context():
        try:
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

            # Seed default settings if empty
            if Setting.query.count() == 0:
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
                    db.session.add(Setting(key=key, value=val, description=desc))

            # Seed initial products if empty
            if Product.query.count() == 0:
                initial_products = [
                    {'name': 'Chicken With Skin', 'category': 'Fresh Chicken', 'price_per_kg': 240.0, 'description': 'Fresh chicken with skin intact. Sourced from Sneha Fresh Chicken.', 'image_url': '/static/images/products/chicken_skin.svg', 'is_available': True},
                    {'name': 'Skinless Chicken', 'category': 'Fresh Chicken', 'price_per_kg': 260.0, 'description': 'Tender, skinless fresh chicken cuts prepared hygienically on order.', 'image_url': '/static/images/products/skinless_chicken.svg', 'is_available': True},
                    {'name': 'Chicken Liver', 'category': 'Chicken Organs', 'price_per_kg': 160.0, 'description': 'Fresh, nutrient-rich chicken liver cleaned carefully for your recipes.', 'image_url': '/static/images/products/chicken_liver.svg', 'is_available': True},
                    {'name': 'Chicken Gizzard', 'category': 'Chicken Organs', 'price_per_kg': 160.0, 'description': 'Fresh cleaned chicken gizzard ready for spicy curries and fry dishes.', 'image_url': '/static/images/products/chicken_gizzard.svg', 'is_available': True},
                    {'name': 'Chicken Legs', 'category': 'Special Cuts', 'price_per_kg': 360.0, 'description': 'Juicy drumsticks & full chicken legs ideal for tandoori, fry, or biryani.', 'image_url': '/static/images/products/chicken_legs.svg', 'is_available': True},
                    {'name': 'Chicken Thighs', 'category': 'Special Cuts', 'price_per_kg': 340.0, 'description': 'Flavorful chicken thighs cut according to your culinary preference.', 'image_url': '/static/images/products/chicken_thighs.svg', 'is_available': True},
                    {'name': 'Chicken Breast', 'category': 'Special Cuts', 'price_per_kg': 300.0, 'description': 'Lean, protein-packed fresh chicken breast cut to your exact requirements.', 'image_url': '/static/images/products/chicken_breast.svg', 'is_available': True},
                    {'name': 'Chicken Wings', 'category': 'Special Cuts', 'price_per_kg': 400.0, 'description': 'Tender fresh chicken wings perfect for roasting, grilling, or frying.', 'image_url': '/static/images/products/chicken_wings.svg', 'is_available': True},
                    {'name': 'Boneless Chicken', 'category': 'Special Cuts', 'price_per_kg': 500.0, 'description': '100% pure boneless chicken meat, ideal for chicken 65, kebabs, and curries.', 'image_url': '/static/images/products/boneless_chicken.svg', 'is_available': True}
                ]
                for prod in initial_products:
                    db.session.add(Product(**prod))

            db.session.commit()
        except Exception as e:
            print("Database initialization warning:", e)

    @app.context_processor
    def inject_globals():
        return {
            'settings': get_site_settings(),
            'current_year': datetime.now().year
        }

    # ==================== PUBLIC ROUTES ====================

    @app.route('/')
    def index():
        products = Product.query.filter_by(is_active=True, is_available=True).limit(6).all()
        reviews = Review.query.filter_by(is_approved=True).order_by(Review.created_at.desc()).limit(3).all()
        return render_template('index.html', products=products, reviews=reviews)

    @app.route('/products')
    def products():
        category_filter = request.args.get('category', 'All')
        query = Product.query.filter_by(is_active=True)
        if category_filter != 'All':
            query = query.filter_by(category=category_filter)
        all_products = query.order_by(Product.id.asc()).all()
        categories = ['All', 'Fresh Chicken', 'Special Cuts', 'Chicken Organs']
        return render_template('products.html', products=all_products, categories=categories, selected_category=category_filter)

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/bulk-orders')
    def bulk_orders():
        return render_template('bulk_orders.html')

    @app.route('/reviews')
    def reviews():
        approved_reviews = Review.query.filter_by(is_approved=True).order_by(Review.created_at.desc()).all()
        return render_template('reviews.html', reviews=approved_reviews)

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    # ==================== CUSTOMER APIS ====================

    @app.route('/api/order', methods=['POST'])
    def api_create_order():
        try:
            data = request.get_json()
            if not data or not data.get('items'):
                return jsonify({'success': False, 'error': 'No items in order'}), 400

            customer_name = (data.get('customer_name') or '').strip()
            customer_phone = (data.get('customer_phone') or '').strip()
            cutting_preference = (data.get('cutting_preference') or 'Curry Cut').strip()
            special_instructions = (data.get('special_instructions') or '').strip()

            if not customer_name:
                return jsonify({'success': False, 'error': 'Customer name is required'}), 400
            
            clean_phone = ''.join(filter(str.isdigit, customer_phone))
            if len(clean_phone) < 10:
                return jsonify({'success': False, 'error': 'Valid 10-digit phone number is required'}), 400

            order_num = "JCC-" + datetime.now().strftime('%Y%m%d') + "-" + str(uuid.uuid4().hex[:4].upper())

            new_order = Order(
                order_number=order_num,
                customer_name=customer_name,
                customer_phone=customer_phone,
                order_type='Pickup',
                status='New',
                payment_method='Cash / UPI on Pickup',
                cutting_preference=cutting_preference,
                special_instructions=special_instructions,
                total_amount=0.0
            )
            db.session.add(new_order)
            db.session.flush()

            total = 0.0
            items_summary = []
            for item_data in data['items']:
                prod_id = item_data.get('product_id')
                prod_name = (item_data.get('product_name') or 'Fresh Chicken Cut').strip()
                qty = max(0.1, float(item_data.get('quantity_kg', 1.0)))
                price = max(0.0, float(item_data.get('price_per_kg', 0.0)))

                if prod_id:
                    prod = Product.query.get(prod_id)
                    if prod and prod.is_active:
                        if not prod.is_available:
                            db.session.rollback()
                            return jsonify({'success': False, 'error': f"Product '{prod.name}' is currently out of stock."}), 400
                        price = prod.price_per_kg
                        prod_name = prod.name

                item_total = round(price * qty, 2)
                total += item_total

                order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=prod_id,
                    product_name=prod_name,
                    quantity_kg=qty,
                    price_per_kg=price,
                    item_total=item_total
                )
                db.session.add(order_item)
                items_summary.append({
                    'name': prod_name,
                    'quantity_kg': qty
                })

            new_order.total_amount = round(total, 2)
            db.session.commit()

            settings = get_site_settings()
            whatsapp_number = settings.get('whatsapp_number', '9908014554')
            whatsapp_url = generate_whatsapp_order_link(
                phone=whatsapp_number,
                customer_name=customer_name,
                items_list=items_summary,
                cutting_preference=cutting_preference,
                special_instructions=special_instructions
            )

            return jsonify({
                'success': True,
                'order_number': order_num,
                'whatsapp_url': whatsapp_url
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/review', methods=['POST'])
    def api_submit_review():
        try:
            name = request.form.get('customer_name') or (request.json.get('customer_name') if request.is_json else None)
            review_text = request.form.get('review_text') or (request.json.get('review_text') if request.is_json else None)
            rating_val = request.form.get('rating') or (request.json.get('rating') if request.is_json else 5)

            if not name or not review_text:
                return jsonify({'success': False, 'error': 'Name and review text are required'}), 400

            try:
                rating = int(rating_val)
            except (ValueError, TypeError):
                rating = 5

            rev = Review(
                customer_name=name.strip(),
                rating=min(5, max(1, rating)),
                review_text=review_text.strip(),
                is_approved=False
            )
            db.session.add(rev)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Thank you! Your review has been submitted and is pending approval.'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/bulk-enquiry', methods=['POST'])
    def api_submit_bulk():
        try:
            contact_name = request.form.get('contact_name') or (request.json.get('contact_name') if request.is_json else None)
            business_name = request.form.get('business_name') or (request.json.get('business_name') if request.is_json else None)
            phone = request.form.get('phone') or (request.json.get('phone') if request.is_json else None)
            business_type = request.form.get('business_type') or (request.json.get('business_type', 'Restaurant / Hotel') if request.is_json else 'Restaurant / Hotel')
            requirement_details = request.form.get('requirement_details') or (request.json.get('requirement_details') if request.is_json else None)

            if not contact_name or not phone or not requirement_details:
                return jsonify({'success': False, 'error': 'Name, phone, and requirements are required'}), 400

            enquiry = BulkEnquiry(
                contact_name=contact_name.strip(),
                business_name=business_name.strip() if business_name else None,
                phone=phone.strip(),
                business_type=business_type,
                requirement_details=requirement_details.strip(),
                status='Pending'
            )
            db.session.add(enquiry)
            db.session.commit()

            settings = get_site_settings()
            wa_num = settings.get('whatsapp_number', '9908014554')
            wa_msg = f"Hello Jahangeer Chicken Center,\n\nBulk Enquiry from: {contact_name}\nBusiness: {business_name or 'N/A'} ({business_type})\nPhone: {phone}\n\nRequirements:\n{requirement_details}\n\nPlease contact me regarding bulk pricing and daily supply."
            wa_url = f"https://wa.me/91{wa_num}?text=" + urllib.parse.quote(wa_msg)

            return jsonify({'success': True, 'message': 'Bulk enquiry submitted successfully.', 'whatsapp_url': wa_url})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/products')
    def api_get_products():
        products = Product.query.filter_by(is_active=True).all()
        return jsonify([p.to_dict() for p in products])

    # ==================== ADMIN AUTHENTICATION ====================

    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if session.get('admin_logged_in'):
            return redirect(url_for('admin_dashboard'))

        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()

            admin = Admin.query.filter_by(username=username).first()
            if admin and admin.check_password(password):
                session['admin_logged_in'] = True
                session['admin_username'] = admin.username
                flash('Successfully logged into Admin Dashboard.', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid username or password. Please try again.', 'danger')

        return render_template('admin/login.html')

    @app.route('/admin/logout')
    def admin_logout():
        session.clear()
        flash('You have been logged out.', 'info')
        return redirect(url_for('admin_login'))

    # ==================== ADMIN DASHBOARD & MANAGEMENT ====================

    @app.route('/admin')
    @app.route('/admin/dashboard')
    @admin_required
    def admin_dashboard():
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=today_start.weekday())
        month_start = today_start.replace(day=1)

        today_revenue = db.session.query(db.func.sum(RevenueTransaction.amount)).filter(RevenueTransaction.transaction_date >= today_start).scalar() or 0.0
        weekly_revenue = db.session.query(db.func.sum(RevenueTransaction.amount)).filter(RevenueTransaction.transaction_date >= week_start).scalar() or 0.0
        monthly_revenue = db.session.query(db.func.sum(RevenueTransaction.amount)).filter(RevenueTransaction.transaction_date >= month_start).scalar() or 0.0
        total_revenue = db.session.query(db.func.sum(RevenueTransaction.amount)).scalar() or 0.0

        today_orders_count = Order.query.filter(Order.created_at >= today_start).count()
        pending_orders_count = Order.query.filter(Order.status.in_(['New', 'Accepted', 'Preparing'])).count()
        completed_orders_count = Order.query.filter_by(status='Completed').count()
        bulk_orders_count = BulkEnquiry.query.count()

        total_chicken_sold_kg = db.session.query(db.func.sum(OrderItem.quantity_kg))\
            .join(Order, OrderItem.order_id == Order.id)\
            .filter(Order.status == 'Completed').scalar() or 0.0

        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
        recent_enquiries = BulkEnquiry.query.order_by(BulkEnquiry.created_at.desc()).limit(5).all()

        kpis = {
            'today_revenue': round(today_revenue, 2),
            'weekly_revenue': round(weekly_revenue, 2),
            'monthly_revenue': round(monthly_revenue, 2),
            'total_revenue': round(total_revenue, 2),
            'today_orders': today_orders_count,
            'pending_orders': pending_orders_count,
            'completed_orders': completed_orders_count,
            'bulk_orders': bulk_orders_count,
            'total_chicken_sold_kg': round(total_chicken_sold_kg, 2)
        }

        return render_template('admin/dashboard.html', kpis=kpis, recent_orders=recent_orders, recent_enquiries=recent_enquiries)

    @app.route('/admin/products', methods=['GET', 'POST'])
    @admin_required
    def admin_products():
        if request.method == 'POST':
            action = request.form.get('action')

            if action == 'add':
                name = request.form.get('name', '').strip()
                category = request.form.get('category', 'Fresh Chicken').strip()
                price = float(request.form.get('price_per_kg', 0.0))
                description = request.form.get('description', '').strip()
                is_available = 'is_available' in request.form

                image_url = '/static/images/products/placeholder.svg'
                if 'image_file' in request.files:
                    file = request.files['image_file']
                    if file and file.filename and allowed_file(file.filename):
                        # Convert to Base64 for serverless persistent database storage
                        file_bytes = file.read()
                        b64_data = base64.b64encode(file_bytes).decode('utf-8')
                        mime = file.mimetype or 'image/jpeg'
                        image_url = f"data:{mime};base64,{b64_data}"

                prod = Product(
                    name=name, category=category, price_per_kg=price,
                    description=description, image_url=image_url, is_available=is_available
                )
                db.session.add(prod)
                db.session.commit()
                flash(f"Product '{name}' added successfully!", 'success')

            elif action == 'edit':
                prod_id = int(request.form.get('product_id'))
                prod = Product.query.get_or_404(prod_id)
                prod.name = request.form.get('name', '').strip()
                prod.category = request.form.get('category', '').strip()
                prod.price_per_kg = float(request.form.get('price_per_kg', 0.0))
                prod.description = request.form.get('description', '').strip()
                prod.is_available = 'is_available' in request.form

                if 'image_file' in request.files:
                    file = request.files['image_file']
                    if file and file.filename and allowed_file(file.filename):
                        file_bytes = file.read()
                        b64_data = base64.b64encode(file_bytes).decode('utf-8')
                        mime = file.mimetype or 'image/jpeg'
                        prod.image_url = f"data:{mime};base64,{b64_data}"

                db.session.commit()
                flash(f"Updated product '{prod.name}' price to ₹{prod.price_per_kg}/kg!", 'success')

            elif action == 'toggle_availability':
                prod_id = int(request.form.get('product_id'))
                prod = Product.query.get_or_404(prod_id)
                prod.is_available = not prod.is_available
                db.session.commit()
                flash(f"Availability for '{prod.name}' updated.", 'info')

            elif action == 'delete':
                prod_id = int(request.form.get('product_id'))
                prod = Product.query.get_or_404(prod_id)
                prod.is_active = False # Soft delete
                db.session.commit()
                flash(f"Product '{prod.name}' deactivated.", 'warning')

            return redirect(url_for('admin_products'))

        products_list = Product.query.filter_by(is_active=True).order_by(Product.id.asc()).all()
        return render_template('admin/products.html', products=products_list)

    @app.route('/admin/orders')
    @admin_required
    def admin_orders():
        status_filter = request.args.get('status', 'All')
        query = Order.query
        if status_filter != 'All':
            query = query.filter_by(status=status_filter)
        orders_list = query.order_by(Order.created_at.desc()).all()
        return render_template('admin/orders.html', orders=orders_list, selected_status=status_filter)

    @app.route('/admin/orders/<int:order_id>/status', methods=['POST'])
    @admin_required
    def admin_update_order_status(order_id):
        order = Order.query.get_or_404(order_id)
        data = request.get_json()
        new_status = data.get('status')

        if new_status and new_status in ['New', 'Accepted', 'Preparing', 'Ready for Pickup', 'Completed', 'Cancelled']:
            old_status = order.status
            order.status = new_status

            if new_status == 'Completed' and old_status != 'Completed':
                existing_tx = RevenueTransaction.query.filter_by(order_id=order.id).first()
                if not existing_tx:
                    rev = RevenueTransaction(
                        amount=order.total_amount,
                        payment_method=order.payment_method,
                        order_type='Website Order Pickup',
                        description=f"Order {order.order_number} for {order.customer_name}",
                        order_id=order.id
                    )
                    db.session.add(rev)
            elif old_status == 'Completed' and new_status != 'Completed':
                RevenueTransaction.query.filter_by(order_id=order.id).delete()

            db.session.commit()
            return jsonify({'success': True, 'status': new_status})

        return jsonify({'success': False, 'error': 'Invalid status'}), 400

    @app.route('/admin/revenue', methods=['GET', 'POST'])
    @admin_required
    def admin_revenue():
        if request.method == 'POST':
            amount = float(request.form.get('amount', 0.0))
            payment_method = request.form.get('payment_method', 'Cash')
            order_type = request.form.get('order_type', 'Retail Walk-in')
            description = request.form.get('description', '')

            if amount > 0:
                rev = RevenueTransaction(
                    amount=amount,
                    payment_method=payment_method,
                    order_type=order_type,
                    description=description
                )
                db.session.add(rev)
                db.session.commit()
                flash(f"Successfully recorded revenue of ₹{amount} ({payment_method})!", 'success')

            return redirect(url_for('admin_revenue'))

        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=today_start.weekday())
        month_start = today_start.replace(day=1)

        today_rev = db.session.query(db.func.sum(RevenueTransaction.amount)).filter(RevenueTransaction.transaction_date >= today_start).scalar() or 0.0
        weekly_rev = db.session.query(db.func.sum(RevenueTransaction.amount)).filter(RevenueTransaction.transaction_date >= week_start).scalar() or 0.0
        monthly_rev = db.session.query(db.func.sum(RevenueTransaction.amount)).filter(RevenueTransaction.transaction_date >= month_start).scalar() or 0.0
        total_rev = db.session.query(db.func.sum(RevenueTransaction.amount)).scalar() or 0.0

        transactions = RevenueTransaction.query.order_by(RevenueTransaction.transaction_date.desc()).all()
        return render_template('admin/revenue.html', transactions=transactions, today_rev=today_rev, weekly_rev=weekly_rev, monthly_rev=monthly_rev, total_rev=total_rev)

    @app.route('/admin/bulk')
    @admin_required
    def admin_bulk():
        enquiries = BulkEnquiry.query.order_by(BulkEnquiry.created_at.desc()).all()
        return render_template('admin/bulk.html', enquiries=enquiries)

    @app.route('/admin/bulk/<int:enquiry_id>/status', methods=['POST'])
    @admin_required
    def admin_update_bulk_status(enquiry_id):
        enquiry = BulkEnquiry.query.get_or_404(enquiry_id)
        data = request.get_json()
        enquiry.status = data.get('status', enquiry.status)
        if 'notes' in data:
            enquiry.notes = data.get('notes')
        db.session.commit()
        return jsonify({'success': True})

    @app.route('/admin/reviews')
    @admin_required
    def admin_reviews():
        reviews_list = Review.query.order_by(Review.created_at.desc()).all()
        return render_template('admin/reviews.html', reviews=reviews_list)

    @app.route('/admin/reviews/<int:review_id>/action', methods=['POST'])
    @admin_required
    def admin_review_action(review_id):
        rev = Review.query.get_or_404(review_id)
        action = request.form.get('action')
        if action == 'approve':
            rev.is_approved = True
            flash('Review approved and published on website.', 'success')
        elif action == 'hide':
            rev.is_approved = False
            flash('Review hidden from website.', 'info')
        elif action == 'delete':
            db.session.delete(rev)
            flash('Review deleted.', 'warning')
        db.session.commit()
        return redirect(url_for('admin_reviews'))

    @app.route('/admin/settings', methods=['GET', 'POST'])
    @admin_required
    def admin_settings():
        if request.method == 'POST':
            for key in ['shop_name', 'phone_primary', 'phone_secondary', 'whatsapp_number', 'address_line', 'opening_hours', 'maps_url', 'instagram_url']:
                val = request.form.get(key)
                if val is not None:
                    s = Setting.query.filter_by(key=key).first()
                    if not s:
                        s = Setting(key=key, value=val)
                        db.session.add(s)
                    else:
                        s.value = val

            new_pass = request.form.get('new_password')
            if new_pass and new_pass.strip():
                admin = Admin.query.filter_by(username=session.get('admin_username')).first()
                if admin:
                    admin.set_password(new_pass.strip())
                    flash('Admin password changed successfully!', 'success')

            db.session.commit()
            flash('Website settings saved successfully!', 'success')
            return redirect(url_for('admin_settings'))

        return render_template('admin/settings.html')

    # ==================== ADMIN CHART APIS ====================

    @app.route('/admin/api/revenue-analytics')
    @admin_required
    def admin_api_revenue():
        today = datetime.now().date()
        labels = []
        revenue_data = []

        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            labels.append(day.strftime('%b %d'))

            day_start = datetime.combine(day, datetime.min.time())
            day_end = datetime.combine(day, datetime.max.time())

            total = db.session.query(db.func.sum(RevenueTransaction.amount))\
                .filter(RevenueTransaction.transaction_date >= day_start)\
                .filter(RevenueTransaction.transaction_date <= day_end).scalar() or 0.0

            revenue_data.append(round(total, 2))

        return jsonify({'labels': labels, 'revenue': revenue_data})

    @app.route('/admin/api/product-analytics')
    @admin_required
    def admin_api_product_sales():
        items = db.session.query(OrderItem.product_name, db.func.sum(OrderItem.quantity_kg))\
            .join(Order, OrderItem.order_id == Order.id)\
            .filter(Order.status == 'Completed')\
            .group_by(OrderItem.product_name).all()

        labels = [item[0] for item in items] if items else ['Skinless Chicken', 'Chicken With Skin', 'Boneless Chicken', 'Chicken Legs', 'Chicken Breast']
        data = [round(item[1], 2) for item in items] if items else [0, 0, 0, 0, 0]

        return jsonify({'labels': labels, 'data': data})

    # ==================== ERROR HANDLERS ====================

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app

# Module-level app instance for Vercel WSGI entrypoint
app = create_app()

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='127.0.0.1', port=5000, debug=debug_mode)
