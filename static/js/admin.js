/**
 * Jahangeer Chicken Center - Admin Dashboard Interactivity & Charts
 */

document.addEventListener('DOMContentLoaded', () => {
  initRevenueChart();
  initProductSalesChart();
});

function initRevenueChart() {
  const ctx = document.getElementById('revenueTrendChart');
  if (!ctx) return;

  fetch('/admin/api/revenue-analytics')
    .then(res => res.json())
    .then(data => {
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.labels || ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
          datasets: [{
            label: 'Revenue (₹)',
            data: data.revenue || [0, 0, 0, 0, 0, 0, 0],
            borderColor: '#F59E0B',
            backgroundColor: 'rgba(245, 158, 11, 0.1)',
            fill: true,
            tension: 0.3,
            borderWidth: 3,
            pointBackgroundColor: '#D97706',
            pointRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: function(value) { return '₹' + value; }
              }
            }
          }
        }
      });
    })
    .catch(err => console.error("Error loading revenue analytics", err));
}

function initProductSalesChart() {
  const ctx = document.getElementById('productSalesChart');
  if (!ctx) return;

  fetch('/admin/api/product-analytics')
    .then(res => res.json())
    .then(data => {
      new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: data.labels || ['Skinless', 'With Skin', 'Boneless', 'Legs', 'Breast', 'Others'],
          datasets: [{
            data: data.data || [0, 0, 0, 0, 0, 0],
            backgroundColor: [
              '#EF4444', '#F59E0B', '#10B981', '#3B82F6', '#8B5CF6', '#64748B'
            ]
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom' }
          }
        }
      });
    })
    .catch(err => console.error("Error loading product analytics", err));
}

function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('hidden');
    modal.classList.add('flex');
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
  }
}

function editProductModal(product) {
  document.getElementById('edit-product-id').value = product.id;
  document.getElementById('edit-product-name').value = product.name;
  document.getElementById('edit-product-category').value = product.category;
  document.getElementById('edit-product-price').value = product.price_per_kg;
  document.getElementById('edit-product-description').value = product.description;
  document.getElementById('edit-product-available').checked = product.is_available;
  
  openModal('editProductModal');
}

function updateOrderStatus(orderId, newStatus) {
  fetch(`/admin/orders/${orderId}/status`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: newStatus })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      location.reload();
    } else {
      alert("Error updating order status: " + data.error);
    }
  })
  .catch(err => alert("Network error while updating status"));
}

function updateBulkStatus(enquiryId, newStatus) {
  fetch(`/admin/bulk/${enquiryId}/status`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: newStatus })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      location.reload();
    } else {
      alert("Error updating bulk enquiry status");
    }
  });
}
