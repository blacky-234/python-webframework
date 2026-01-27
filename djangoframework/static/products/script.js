// scripts.js

// -------- CSRF helper --------------------------------
function getCookie(name) {
  const v = document.cookie.split('; ').find(row => row.startsWith(name + '='));
  return v ? decodeURIComponent(v.split('=')[1]) : null;
}
const csrftoken = getCookie('csrftoken');

// default fetch options helper
function apiFetch(url, options = {}) {
  options.headers = options.headers || {};
  if (!['GET','HEAD'].includes((options.method||'GET').toUpperCase())) {
    options.headers['X-CSRFToken'] = csrftoken;
    options.headers['Content-Type'] = 'application/json';
  }
  return fetch(url, options).then(r => r.json());
}

// -------- Common: load categories into selects ----------
function loadCategories(selectEl) {
  // Assumes you have API endpoint to list categories: /categories/ (or create one)
  fetch('/categories/')
    .then(r => r.json())
    .then(data => {
      const list = Array.isArray(data) ? data : (data.results || data);
      list.forEach(cat => {
        const opt = document.createElement('option');
        opt.value = cat.id;
        opt.textContent = cat.name;
        selectEl.appendChild(opt);
      });
    })
    .catch(err => console.error('loadCategories', err));
}

// -------- PRODUCTS PAGE logic -------------------------
if (document.querySelector('#products_list')) {
  let page = 1, page_size = 6;

  const productsEl = document.getElementById('products_list');
  const categoryFilter = document.getElementById('category_filter');
  const searchInput = document.getElementById('search');
  const minPrice = document.getElementById('min_price');
  const maxPrice = document.getElementById('max_price');
  const stockInput = document.getElementById('stock');
  const pageInfo = document.getElementById('page_info');
  const prevBtn = document.getElementById('prev_page');
  const nextBtn = document.getElementById('next_page');

  loadCategories(categoryFilter);

  function buildQuery() {
    const q = new URLSearchParams();
    q.set('page', page);
    q.set('page_size', page_size);
    if (categoryFilter.value) q.set('category', categoryFilter.value);
    if (searchInput.value) q.set('search', searchInput.value);
    if (minPrice.value) q.set('min_price', minPrice.value);
    if (maxPrice.value) q.set('max_price', maxPrice.value);
    if (stockInput.value) q.set('stock', stockInput.value);
    return q.toString();
  }

  function renderProducts(list) {
    productsEl.innerHTML = '';
    if (!list || list.length === 0) {
      productsEl.innerHTML = '<em>No products found</em>';
      return;
    }
    list.forEach(p => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = `
        <h4>${p.name}</h4>
        <div>Price: ₹${p.price}</div>
        <div>Stock: ${p.stock}</div>
        <div>Category: ${p.category_name || ''}</div>
        <div class="actions">
          <button class="order_btn" data-id="${p.id}" data-name="${p.name}">Order</button>
          <button class="edit_btn" data-id="${p.id}">Edit</button>
          <button class="del_btn" data-id="${p.id}">Delete</button>
        </div>
      `;
      productsEl.appendChild(card);
    });
  }

  function loadProducts() {
    const q = buildQuery();
    fetch(`/products/?${q}`)
      .then(r => r.json())
      .then(data => {
        // response format from our earlier API: total, pages, current_page, results
        const results = data.results || data;
        renderProducts(results);
        pageInfo.textContent = `Page ${data.current_page || page} of ${data.pages || '-'}`;
        prevBtn.disabled = (data.current_page || page) <= 1;
        nextBtn.disabled = (data.current_page || page) >= (data.pages || 1);
      });
  }

  // initial load
  loadProducts();

  // events
  document.getElementById('apply_filters').addEventListener('click', () => { page = 1; loadProducts(); });
  document.getElementById('clear_filters').addEventListener('click', () => {
    categoryFilter.value = ''; searchInput.value = ''; minPrice.value = ''; maxPrice.value = ''; stockInput.value = '';
    page = 1; loadProducts();
  });
  prevBtn.addEventListener('click', () => { page = Math.max(1, page - 1); loadProducts(); });
  nextBtn.addEventListener('click', () => { page = page + 1; loadProducts(); });

  // delegated clicks for order/edit/delete
  productsEl.addEventListener('click', (e) => {
    const target = e.target;
    if (target.classList.contains('order_btn')) {
      openOrderModal(target.dataset.id, target.dataset.name);
    } else if (target.classList.contains('edit_btn')) {
      const id = target.dataset.id;
      window.location.href = `/ui/product/form/?id=${id}`;
    } else if (target.classList.contains('del_btn')) {
      const id = target.dataset.id;
      if (!confirm('Delete product?')) return;
      apiFetch(`/product/delete/${id}/`, { method: 'DELETE' })
        .then(res => { alert(res.message || 'Deleted'); loadProducts(); })
        .catch(err => console.error(err));
    }
  });

  // ----- Order modal logic -----
  const orderModal = document.getElementById('order_modal');
  const orderName = document.getElementById('order_product_name');
  const orderQty = document.getElementById('order_qty');
  const placeOrderBtn = document.getElementById('place_order');
  const cancelOrderBtn = document.getElementById('cancel_order');
  const orderMsg = document.getElementById('order_msg');
  let currentProductId = null;

  function openOrderModal(id, name) {
    currentProductId = id;
    orderName.textContent = name;
    orderQty.value = 1;
    orderMsg.textContent = '';
    orderModal.classList.remove('hidden');
  }
  cancelOrderBtn.addEventListener('click', () => orderModal.classList.add('hidden'));
  placeOrderBtn.addEventListener('click', () => {
    const qty = parseInt(orderQty.value) || 1;
    apiFetch('/order/add/', {
      method: 'POST',
      body: JSON.stringify({ product: currentProductId, qty })
    }).then(res => {
      if (res.id || res.data) {
        orderMsg.textContent = 'Order placed';
        loadProducts();
        setTimeout(()=> orderModal.classList.add('hidden'), 800);
      } else {
        orderMsg.textContent = JSON.stringify(res);
      }
    }).catch(err => { orderMsg.textContent = 'Error'; console.error(err); });
  });
}



// -------- PRODUCT FORM PAGE logic -------------------------
if (document.querySelector('#product_form')) {
  const qParams = new URLSearchParams(window.location.search);
  const productId = qParams.get('id');
  const form = document.getElementById('product_form');
  const title = document.getElementById('form_title');
  const msg = document.getElementById('form_msg');
  const catSelect = document.getElementById('p_category');

  loadCategories(catSelect);

  if (productId) {
    title.textContent = 'Edit Product';
    // load existing product data
    fetch(`/products/?page=1&page_size=1000`) // crude: load all and find id (or create /product/<id>/ GET)
      .then(r => r.json())
      .then(data => {
        const list = data.results || data;
        const p = list.find(x => String(x.id) === String(productId));
        if (p) {
          document.getElementById('p_name').value = p.name;
          document.getElementById('p_price').value = p.price;
          document.getElementById('p_stock').value = p.stock;
          // wait a little for categories to load and then set value
          setTimeout(()=> { if (p.category) catSelect.value = p.category; }, 300);
        }
      });
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const payload = {
      name: document.getElementById('p_name').value,
      price: document.getElementById('p_price').value,
      stock: document.getElementById('p_stock').value,
      category: document.getElementById('p_category').value
    };

    if (productId) {
      apiFetch(`/product/update/${productId}/`, { method: 'PUT', body: JSON.stringify(payload) })
        .then(res => {
          if (res.data || res.id) {
            msg.textContent = 'Updated successfully';
            setTimeout(()=> window.location.href = '/ui/products/', 700);
          } else {
            msg.textContent = JSON.stringify(res);
          }
        }).catch(err=> { msg.textContent='Error'; console.error(err); });
    } else {
      apiFetch('/product/add/', { method: 'POST', body: JSON.stringify(payload) })
        .then(res => {
          if (res.data || res.id) {
            msg.textContent = 'Created';
            setTimeout(()=> window.location.href = '/ui/products/', 700);
          } else {
            msg.textContent = JSON.stringify(res);
          }
        }).catch(err=> { msg.textContent='Error'; console.error(err); });
    }
  });

  document.getElementById('cancel_btn').addEventListener('click', ()=> window.location.href = '/ui/products/');
}

// -------- ORDERS PAGE logic -------------------------
if (document.querySelector('#orders_list')) {
  const ordersEl = document.getElementById('orders_list');
  function loadOrders() {
    fetch('/orders/')
      .then(r => r.json())
      .then(data => {
        const list = Array.isArray(data) ? data : (data.results || data);
        ordersEl.innerHTML = '';
        if (!list || list.length === 0) {
          ordersEl.innerHTML = '<em>No orders</em>';
          return;
        }
        list.forEach(o => {
          const c = document.createElement('div'); c.className = 'card';
          c.innerHTML = `<div>Product: ${o.product_name || ''}</div>
                         <div>Qty: ${o.qty}</div>
                         <div>Total: ₹${o.total}</div>
                         <div>When: ${new Date(o.created_at).toLocaleString()}</div>`;
          ordersEl.appendChild(c);
        });
      });
  }
  loadOrders();
}
