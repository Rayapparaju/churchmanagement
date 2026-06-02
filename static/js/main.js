document.addEventListener('DOMContentLoaded', function () {
    initSidebar();
    initAutoDismissAlerts();
    initConfirmDeletes();
    initDataTableSearch();
    initFormValidation();
    initPrintButtons();
});

/* ===== Sidebar Toggle ===== */
function initSidebar() {
    const toggleBtn = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');

    if (!toggleBtn || !sidebar) return;

    toggleBtn.addEventListener('click', function (e) {
        e.preventDefault();
        sidebar.classList.toggle('collapsed');
        if (window.innerWidth <= 991.98) {
            sidebar.classList.toggle('expanded');
        }
        const isCollapsed = sidebar.classList.contains('collapsed');
        localStorage.setItem('sidebarCollapsed', isCollapsed ? 'true' : 'false');
    });

    const savedState = localStorage.getItem('sidebarCollapsed');
    if (savedState === 'true' && window.innerWidth > 991.98) {
        sidebar.classList.add('collapsed');
    }

    document.addEventListener('click', function (e) {
        if (window.innerWidth <= 991.98) {
            const isClickInside = sidebar.contains(e.target) || toggleBtn.contains(e.target);
            if (!isClickInside && sidebar.classList.contains('expanded')) {
                sidebar.classList.remove('expanded');
            }
        }
    });
}

/* ===== Auto-Dismiss Alerts ===== */
function initAutoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert-dismissible:not(.alert-permanent)');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/* ===== Confirm Delete Modals ===== */
function initConfirmDeletes() {
    document.body.addEventListener('click', function (e) {
        const deleteBtn = e.target.closest('[data-confirm-delete]');
        if (!deleteBtn) return;

        e.preventDefault();
        const message = deleteBtn.getAttribute('data-confirm-message') || 'Are you sure you want to delete this item? This action cannot be undone.';
        const title = deleteBtn.getAttribute('data-confirm-title') || 'Confirm Delete';
        const form = deleteBtn.closest('form') || document.getElementById(deleteBtn.getAttribute('data-form-id'));

        showConfirmModal(title, message, function () {
            if (form) {
                form.submit();
            } else {
                window.location.href = deleteBtn.getAttribute('href');
            }
        });
    });
}

function showConfirmModal(title, message, onConfirm) {
    const modalEl = document.getElementById('confirmDeleteModal');
    if (modalEl) {
        modalEl.querySelector('.modal-title').textContent = title;
        modalEl.querySelector('.modal-body').innerHTML = '<p>' + message + '</p>';
        const confirmBtn = modalEl.querySelector('.btn-confirm-delete');
        const newConfirmBtn = confirmBtn.cloneNode(true);
        confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
        newConfirmBtn.addEventListener('click', function () {
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();
            if (typeof onConfirm === 'function') onConfirm();
        });
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
        return;
    }

    const modalHtml = `
        <div class="modal fade" id="dynamicConfirmModal" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${escapeHtml(title)}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>${escapeHtml(message)}</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-accent btn-confirm-delete">Delete</button>
                    </div>
                </div>
            </div>
        </div>`;

    const wrapper = document.createElement('div');
    wrapper.innerHTML = modalHtml;
    document.body.appendChild(wrapper);
    const modalEl2 = document.getElementById('dynamicConfirmModal');
    const confirmBtn2 = modalEl2.querySelector('.btn-confirm-delete');
    confirmBtn2.addEventListener('click', function () {
        const modal = bootstrap.Modal.getInstance(modalEl2);
        if (modal) modal.hide();
        modalEl2.addEventListener('hidden.bs.modal', function () {
            modalEl2.remove();
        });
        if (typeof onConfirm === 'function') onConfirm();
    });
    const modal = new bootstrap.Modal(modalEl2);
    modal.show();
}

/* ===== Data Table Search / Filter ===== */
function initDataTableSearch() {
    const searchInput = document.getElementById('tableSearch');
    const table = document.querySelector('.table.table-searchable');
    if (!searchInput || !table) return;

    searchInput.addEventListener('keyup', function () {
        const query = this.value.toLowerCase().trim();
        const rows = table.querySelectorAll('tbody tr');

        rows.forEach(function (row) {
            let found = false;
            const cells = row.querySelectorAll('td');
            cells.forEach(function (cell) {
                if (cell.textContent.toLowerCase().indexOf(query) !== -1) {
                    found = true;
                }
            });
            row.style.display = found ? '' : 'none';
        });

        const visibleRows = table.querySelectorAll('tbody tr:not([style*="display: none"])');
        const noResultsRow = table.querySelector('.no-results-row');
        if (visibleRows.length === 0) {
            if (!noResultsRow) {
                const row = document.createElement('tr');
                row.className = 'no-results-row';
                const colSpan = (table.querySelector('thead tr th') || {}).length || 1;
                row.innerHTML = '<td colspan="' + colSpan + '" class="text-center py-4 text-muted">No matching records found</td>';
                table.querySelector('tbody').appendChild(row);
            }
        } else if (noResultsRow) {
            noResultsRow.remove();
        }
    });
}

/* ===== Form Validation Enhancement ===== */
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    document.querySelectorAll('input, select, textarea').forEach(function (input) {
        input.addEventListener('blur', function () {
            if (this.closest('.needs-validation')) {
                if (this.checkValidity()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                } else if (this.value) {
                    this.classList.remove('is-valid');
                    this.classList.add('is-invalid');
                }
            }
        });
    });
}

/* ===== Print Functionality ===== */
function initPrintButtons() {
    document.body.addEventListener('click', function (e) {
        const printBtn = e.target.closest('[data-print]');
        if (!printBtn) return;
        e.preventDefault();
        window.print();
    });
}

/* ===== Utility: Show Loading Spinner ===== */
function showSpinner(message) {
    message = message || 'Loading...';
    let overlay = document.getElementById('spinnerOverlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'spinnerOverlay';
        overlay.className = 'spinner-overlay';
        overlay.innerHTML = '<div class="spinner-container"><div class="spinner"></div><div class="spinner-text" id="spinnerText"></div></div>';
        document.body.appendChild(overlay);
    }
    overlay.querySelector('#spinnerText').textContent = message;
    overlay.classList.add('active');
}

function hideSpinner() {
    const overlay = document.getElementById('spinnerOverlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
}

/* ===== Utility: Escape HTML ===== */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
}

/* ===== Utility: Fetch API helper ===== */
async function apiFetch(url, options) {
    options = options || {};
    options.headers = options.headers || {};
    options.headers['X-Requested-With'] = 'XMLHttpRequest';

    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    if (csrfMeta) {
        options.headers['X-CSRFToken'] = csrfMeta.getAttribute('content');
    }

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            const errorData = await response.json().catch(function () { return null; });
            throw new Error((errorData && errorData.message) || 'Request failed with status ' + response.status);
        }
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/* ===== Utility: Format Date ===== */
function formatDate(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatDateTime(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}
