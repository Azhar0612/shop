/**
 * Jahangeer Chicken Center - Customer Pickup Cart & WhatsApp Order Builder
 */

let cart = [];
let shopPhone = '9908014554';

document.addEventListener('DOMContentLoaded', () => {
  renderCartUI();
});

function addToCart(productId, name, price, defaultQty = 1) {
  const existing = cart.find(item => item.id === productId);
  if (existing) {
    existing.quantity = Math.round((existing.quantity + defaultQty) * 10) / 10;
  } else {
    cart.push({
      id: productId,
      name: name,
      price: price,
      quantity: defaultQty
    });
  }
  renderCartUI();
  openCartDrawer();
  showToast(`${name} added to order!`);
}

function updateCartQuantity(productId, delta) {
  const item = cart.find(i => i.id === productId);
  if (item) {
    item.quantity = Math.max(0.5, Math.round((item.quantity + delta) * 10) / 10);
    renderCartUI();
  }
}

function setCartQuantity(productId, qty) {
  const item = cart.find(i => i.id === productId);
  if (item) {
    const val = parseFloat(qty);
    item.quantity = isNaN(val) || val < 0.1 ? 0.5 : Math.round(val * 10) / 10;
    renderCartUI();
  }
}

function removeFromCart(productId) {
  cart = cart.filter(i => i.id !== productId);
  renderCartUI();
}

function clearCart() {
  cart = [];
  renderCartUI();
}

function renderCartUI() {
  const cartContainer = document.getElementById('cart-items-list');
  const cartTotalEl = document.getElementById('cart-total-amount');
  const cartBadgeEl = document.getElementById('cart-badge-count');

  if (!cartContainer) return;

  if (cartBadgeEl) {
    cartBadgeEl.textContent = cart.length;
    cartBadgeEl.style.display = cart.length > 0 ? 'inline-flex' : 'none';
  }

  if (cart.length === 0) {
    cartContainer.innerHTML = `
      <div class="text-center py-8 text-slate-500">
        <svg class="w-12 h-12 mx-auto mb-3 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/>
        </svg>
        <p class="font-medium" data-i18n="cart_empty">Your order is empty. Select products below.</p>
      </div>
    `;
    if (cartTotalEl) cartTotalEl.textContent = '₹0.00';
    return;
  }

  let totalAmount = 0;
  let html = '';

  cart.forEach(item => {
    const itemTotal = Math.round(item.price * item.quantity * 100) / 100;
    totalAmount += itemTotal;

    html += `
      <div class="flex items-center justify-between p-3 bg-slate-50 rounded-xl border border-slate-200 mb-2">
        <div class="flex-1 pr-2">
          <h4 class="font-bold text-slate-800 text-sm">${item.name}</h4>
          <p class="text-xs text-amber-600 font-semibold">₹${item.price} / kg</p>
        </div>
        
        <div class="flex items-center gap-2">
          <div class="flex items-center border border-slate-300 rounded-lg bg-white overflow-hidden">
            <button onclick="updateCartQuantity(${item.id}, -0.5)" class="px-2.5 py-1 text-slate-600 hover:bg-slate-100 font-bold text-sm">-</button>
            <input type="number" step="0.5" min="0.5" value="${item.quantity}" 
                   onchange="setCartQuantity(${item.id}, this.value)" 
                   class="w-12 text-center text-xs font-semibold py-1 focus:outline-none border-x border-slate-200">
            <button onclick="updateCartQuantity(${item.id}, 0.5)" class="px-2.5 py-1 text-slate-600 hover:bg-slate-100 font-bold text-sm">+</button>
          </div>
          <span class="text-xs font-bold text-slate-700 min-w-[55px] text-right">₹${itemTotal.toFixed(0)}</span>
          <button onclick="removeFromCart(${item.id})" class="text-slate-400 hover:text-red-600 p-1" title="Remove">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
          </button>
        </div>
      </div>
    `;
  });

  cartContainer.innerHTML = html;
  if (cartTotalEl) cartTotalEl.textContent = `₹${totalAmount.toFixed(0)}`;
}

function submitCartOrder() {
  if (cart.length === 0) {
    alert("Please add at least one product to your order.");
    return;
  }

  const customerNameEl = document.getElementById('cart-customer-name');
  const customerPhoneEl = document.getElementById('cart-customer-phone');
  const cuttingPrefEl = document.getElementById('cart-cutting-preference');
  const instructionsEl = document.getElementById('cart-special-instructions');

  const customerName = customerNameEl ? customerNameEl.value.trim() : '';
  const customerPhone = customerPhoneEl ? customerPhoneEl.value.trim() : '';
  const cuttingPref = cuttingPrefEl ? cuttingPrefEl.value : 'Curry Cut';
  const specialInstructions = instructionsEl ? instructionsEl.value.trim() : '';

  if (!customerName) {
    alert("Please enter your name so we can prepare your order.");
    if (customerNameEl) customerNameEl.focus();
    return;
  }

  const cleanPhone = customerPhone.replace(/\D/g, '');
  if (!cleanPhone || cleanPhone.length < 10) {
    alert("Please enter a valid 10-digit phone number.");
    if (customerPhoneEl) customerPhoneEl.focus();
    return;
  }

  const orderData = {
    customer_name: customerName,
    customer_phone: customerPhone,
    cutting_preference: cuttingPref,
    special_instructions: specialInstructions,
    items: cart.map(i => ({
      product_id: i.id,
      product_name: i.name,
      quantity_kg: i.quantity,
      price_per_kg: i.price
    }))
  };

  fetch('/api/order', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(orderData)
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      showToast("Order submitted! Opening WhatsApp...");
      clearCart();
      closeCartDrawer();
      if (data.whatsapp_url) {
        window.open(data.whatsapp_url, '_blank');
      }
    } else {
      alert("Failed to create order: " + (data.error || "Unknown error"));
    }
  })
  .catch(err => {
    console.error(err);
    alert("An error occurred while submitting order. Opening direct WhatsApp...");
    generateFallbackWhatsApp(customerName, cuttingPref, specialInstructions);
  });
}

function generateFallbackWhatsApp(name, cutting, instructions) {
  let text = `Hello Jahangeer Chicken Center,\n\nName: ${name}\nI would like to order:\n`;
  cart.forEach(i => {
    text += `• ${i.name} - ${i.quantity} kg\n`;
  });
  text += `\nCutting preference: ${cutting}\n`;
  if (instructions) text += `Special instructions: ${instructions}\n`;
  text += `\nI will pick it up from the shop.\nThank you.`;

  const url = `https://wa.me/919908014554?text=${encodeURIComponent(text)}`;
  window.open(url, '_blank');
}

function openCartDrawer() {
  const drawer = document.getElementById('cart-drawer');
  if (drawer) {
    drawer.classList.remove('translate-x-full');
    drawer.classList.add('translate-x-0');
  }
}

function closeCartDrawer() {
  const drawer = document.getElementById('cart-drawer');
  if (drawer) {
    drawer.classList.remove('translate-x-0');
    drawer.classList.add('translate-x-full');
  }
}

function showToast(message) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = 'bg-slate-900 text-white text-sm font-semibold px-4 py-3 rounded-xl shadow-lg flex items-center gap-2 transform transition-all duration-300 translate-y-2 opacity-0';
  toast.innerHTML = `
    <svg class="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
    </svg>
    <span>${message}</span>
  `;
  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.remove('translate-y-2', 'opacity-0');
  }, 10);

  setTimeout(() => {
    toast.classList.add('opacity-0', 'translate-y-2');
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}
