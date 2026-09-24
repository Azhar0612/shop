import os

os.makedirs('static/images/products', exist_ok=True)

products = [
    ('chicken_skin', 'Chicken With Skin', '#FEF3C7', '#D97706', 'Whole & Curry Cut Chicken with Fresh Skin'),
    ('skinless_chicken', 'Skinless Chicken', '#FEE2E2', '#DC2626', 'Fresh Skinless Chicken Curry Cut'),
    ('chicken_liver', 'Chicken Liver', '#FCE7F3', '#BE185D', 'Fresh Nutrient-Rich Chicken Liver'),
    ('chicken_gizzard', 'Chicken Gizzard', '#FFEDD5', '#C2410C', 'Fresh Cleaned Chicken Gizzard'),
    ('chicken_legs', 'Chicken Legs', '#FEF3C7', '#B45309', 'Juicy Fresh Drumsticks & Legs'),
    ('chicken_thighs', 'Chicken Thighs', '#FFFBEB', '#D97706', 'Tender Fresh Chicken Thigh Cuts'),
    ('chicken_breast', 'Chicken Breast', '#F1F5F9', '#475569', 'Lean Fresh Chicken Breast Meat'),
    ('chicken_wings', 'Chicken Wings', '#FEF3C7', '#EA580C', 'Fresh Chicken Wings'),
    ('boneless_chicken', 'Boneless Chicken', '#FEE2E2', '#B91C1C', '100% Pure Boneless Fresh Meat'),
    ('placeholder', 'Fresh Chicken', '#F8FAFC', '#64748B', 'Jahangeer Chicken Center Fresh Product')
]

svg_template = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 350" width="100%" height="100%">
  <rect width="500" height="350" rx="16" fill="{bg_color}" />
  <circle cx="250" cy="150" r="90" fill="#FFFFFF" opacity="0.9" stroke="{accent_color}" stroke-width="4" stroke-dasharray="6,4"/>
  <path d="M 250 80 C 270 100, 280 120, 275 145 C 290 140, 305 148, 300 165 C 310 175, 305 195, 285 200 C 290 220, 270 230, 250 225 C 230 230, 210 220, 215 200 C 195 195, 190 175, 200 165 C 195 148, 210 140, 225 145 C 220 120, 230 100, 250 80 Z" fill="{accent_color}" />
  
  <rect x="30" y="260" width="440" height="65" rx="12" fill="#FFFFFF" shadow="0 4px 6px -1px rgba(0,0,0,0.1)"/>
  <text x="250" y="290" font-family="'Plus Jakarta Sans', Arial, sans-serif" font-weight="800" font-size="22" fill="#0F172A" text-anchor="middle">{title}</text>
  <text x="250" y="312" font-family="'Inter', sans-serif" font-weight="600" font-size="13" fill="#64748B" text-anchor="middle">{sub}</text>
</svg>"""

for filename, title, bg, accent, sub in products:
    content = svg_template.format(bg_color=bg, accent_color=accent, title=title, sub=sub)
    with open(f'static/images/products/{filename}.svg', 'w', encoding='utf-8') as f:
        f.write(content)

print("Generated product SVGs successfully.")
