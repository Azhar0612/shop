import os

os.makedirs('static/images/products', exist_ok=True)

# Generator for 9 distinct, valid SVG illustrations for each product cut
svg_data = {
    'chicken_skin': {
        'title': 'Chicken With Skin',
        'sub': 'Fresh Whole & Curry Cut with Skin',
        'bg': '#FFFBEB',
        'badge_bg': '#FEF3C7',
        'accent': '#D97706',
        'meat_color': '#F59E0B',
        'icon': 'whole'
    },
    'skinless_chicken': {
        'title': 'Skinless Chicken',
        'sub': 'Fresh Hygienic Skinless Curry Cut',
        'bg': '#FEF2F2',
        'badge_bg': '#FEE2E2',
        'accent': '#DC2626',
        'meat_color': '#EF4444',
        'icon': 'skinless'
    },
    'chicken_liver': {
        'title': 'Chicken Liver',
        'sub': 'Fresh Nutrient-Rich Organ Cut',
        'bg': '#FDF2F8',
        'badge_bg': '#FCE7F3',
        'accent': '#BE185D',
        'meat_color': '#9D174D',
        'icon': 'liver'
    },
    'chicken_gizzard': {
        'title': 'Chicken Gizzard',
        'sub': 'Fresh Cleaned Gizzard for Curries',
        'bg': '#FFF7ED',
        'badge_bg': '#FFEDD5',
        'accent': '#C2410C',
        'meat_color': '#EA580C',
        'icon': 'gizzard'
    },
    'chicken_legs': {
        'title': 'Chicken Legs',
        'sub': 'Juicy Drumsticks & Leg Cuts',
        'bg': '#FFFBEB',
        'badge_bg': '#FEF3C7',
        'accent': '#B45309',
        'meat_color': '#D97706',
        'icon': 'legs'
    },
    'chicken_thighs': {
        'title': 'Chicken Thighs',
        'sub': 'Tender Meat Thigh Cuts',
        'bg': '#FEF3C7',
        'badge_bg': '#FDE68A',
        'accent': '#D97706',
        'meat_color': '#B45309',
        'icon': 'thighs'
    },
    'chicken_breast': {
        'title': 'Chicken Breast',
        'sub': 'Lean Protein Fillet Cuts',
        'bg': '#F8FAFC',
        'badge_bg': '#F1F5F9',
        'accent': '#475569',
        'meat_color': '#64748B',
        'icon': 'breast'
    },
    'chicken_wings': {
        'title': 'Chicken Wings',
        'sub': 'Fresh Wing Cuts for Grilling & Frying',
        'bg': '#FFF7ED',
        'badge_bg': '#FFEDD5',
        'accent': '#EA580C',
        'meat_color': '#C2410C',
        'icon': 'wings'
    },
    'boneless_chicken': {
        'title': 'Boneless Chicken',
        'sub': '100% Pure Boneless Meat Cubes',
        'bg': '#FEF2F2',
        'badge_bg': '#FEE2E2',
        'accent': '#B91C1C',
        'meat_color': '#DC2626',
        'icon': 'boneless'
    },
    'placeholder': {
        'title': 'Fresh Chicken Product',
        'sub': 'Jahangeer Chicken Center Secunderabad',
        'bg': '#F8FAFC',
        'badge_bg': '#E2E8F0',
        'accent': '#64748B',
        'meat_color': '#94A3B8',
        'icon': 'placeholder'
    }
}

def generate_svg(key, info):
    title = info['title']
    sub = info['sub']
    bg = info['bg']
    badge_bg = info['badge_bg']
    accent = info['accent']
    meat = info['meat_color']
    icon_type = info['icon']

    # Generate custom SVG graphic shapes based on product cut type
    graphic_content = ""
    if icon_type == 'legs':
        # Drumsticks SVG graphic
        graphic_content = f"""
        <g transform="translate(180, 70)">
          <!-- Drumstick 1 -->
          <path d="M 40 110 C 20 80, 20 40, 50 20 C 80 10, 100 40, 80 80 L 30 130 Z" fill="{meat}" />
          <circle cx="20" cy="140" r="14" fill="#FDE68A" stroke="{accent}" stroke-width="3" />
          <circle cx="35" cy="150" r="14" fill="#FDE68A" stroke="{accent}" stroke-width="3" />
          <!-- Drumstick 2 -->
          <path d="M 100 120 C 80 90, 80 50, 110 30 C 140 20, 160 50, 140 90 L 90 140 Z" fill="{accent}" opacity="0.9" />
          <circle cx="80" cy="150" r="14" fill="#FFFBEB" stroke="{accent}" stroke-width="3" />
          <circle cx="95" cy="160" r="14" fill="#FFFBEB" stroke="{accent}" stroke-width="3" />
        </g>
        """
    elif icon_type == 'boneless':
        # Meat cubes SVG graphic
        graphic_content = f"""
        <g transform="translate(160, 75)">
          <rect x="20" y="20" width="55" height="55" rx="12" fill="{meat}" stroke="#FFFFFF" stroke-width="3"/>
          <rect x="85" y="15" width="60" height="60" rx="14" fill="{accent}" stroke="#FFFFFF" stroke-width="3"/>
          <rect x="35" y="85" width="65" height="65" rx="14" fill="{accent}" opacity="0.85" stroke="#FFFFFF" stroke-width="3"/>
          <rect x="110" y="80" width="50" height="50" rx="12" fill="{meat}" opacity="0.9" stroke="#FFFFFF" stroke-width="3"/>
        </g>
        """
    elif icon_type == 'liver':
        # Liver lobe cuts
        graphic_content = f"""
        <g transform="translate(170, 75)">
          <path d="M 30 50 C 20 20, 70 10, 90 40 C 110 70, 70 100, 40 90 Z" fill="{meat}" />
          <path d="M 80 60 C 70 30, 120 20, 140 50 C 160 80, 120 110, 90 100 Z" fill="{accent}" />
        </g>
        """
    elif icon_type == 'gizzard':
        # Gizzard shapes
        graphic_content = f"""
        <g transform="translate(175, 80)">
          <ellipse cx="50" cy="60" rx="45" ry="35" fill="{meat}" />
          <ellipse cx="110" cy="70" rx="40" ry="30" fill="{accent}" />
          <circle cx="50" cy="60" r="15" fill="#FFFFFF" opacity="0.3" />
          <circle cx="110" cy="70" r="12" fill="#FFFFFF" opacity="0.3" />
        </g>
        """
    elif icon_type == 'breast':
        # Lean breast fillets
        graphic_content = f"""
        <g transform="translate(160, 75)">
          <path d="M 20 70 C 20 20, 100 10, 150 50 C 170 90, 110 120, 40 100 Z" fill="{meat}" stroke="#FFFFFF" stroke-width="3" />
          <path d="M 50 60 C 50 30, 120 20, 160 60 C 170 90, 120 110, 60 90 Z" fill="{accent}" opacity="0.8" />
        </g>
        """
    elif icon_type == 'wings':
        # Chicken wings shape
        graphic_content = f"""
        <g transform="translate(160, 70)">
          <path d="M 30 90 L 80 30 L 140 50 L 160 100 L 100 110 Z" fill="{meat}" stroke="#FFFFFF" stroke-width="3" rx="10"/>
          <circle cx="150" cy="45" r="10" fill="#FDE68A" />
        </g>
        """
    else:
        # Default fresh chicken piece icon
        graphic_content = f"""
        <g transform="translate(175, 70)">
          <circle cx="75" cy="75" r="65" fill="{badge_bg}" stroke="{accent}" stroke-width="4" stroke-dasharray="6,4"/>
          <path d="M 75 30 C 90 45, 100 60, 95 80 C 110 75, 120 85, 115 100 C 100 120, 50 120, 35 100 C 30 85, 40 75, 55 80 C 50 60, 60 45, 75 30 Z" fill="{meat}" />
        </g>
        """

    svg_str = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 350" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad_{key}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg}" />
      <stop offset="100%" stop-color="{badge_bg}" />
    </linearGradient>
  </defs>

  <!-- Card Outer Background -->
  <rect width="500" height="350" rx="20" fill="url(#bgGrad_{key})" />

  <!-- Inner Decorative Circle Badge -->
  <circle cx="250" cy="140" r="100" fill="#FFFFFF" opacity="0.85" stroke="{accent}" stroke-width="3" />

  <!-- Graphic Illustration -->
  {graphic_content}

  <!-- Supplier Fresh Badge Tag -->
  <g transform="translate(160, 20)">
    <rect x="0" y="0" width="180" height="26" rx="13" fill="{accent}" />
    <text x="90" y="17" font-family="'Plus Jakarta Sans', Arial, sans-serif" font-weight="800" font-size="11" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">SNEHA FRESH CHICKEN</text>
  </g>

  <!-- Text Title & Subtitle Banner -->
  <g transform="translate(30, 260)">
    <rect width="440" height="65" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="2"/>
    <text x="220" y="30" font-family="'Plus Jakarta Sans', Arial, sans-serif" font-weight="900" font-size="22" fill="#0F172A" text-anchor="middle">{title}</text>
    <text x="220" y="50" font-family="'Inter', sans-serif" font-weight="600" font-size="13" fill="#64748B" text-anchor="middle">{sub}</text>
  </g>
</svg>"""

    with open(f'static/images/products/{key}.svg', 'w', encoding='utf-8') as f:
        f.write(svg_str)

for key, info in svg_data.items():
    generate_svg(key, info)

print("Generated 10 detailed, fully compliant SVG product illustrations.")
