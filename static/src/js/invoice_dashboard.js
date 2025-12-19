/** @odoo-module */

// Global JavaScript for Invoice Dashboard functionality
(function() {
    'use strict';

    // Wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', function() {
        setupInvoiceDashboard();
    });

    function setupInvoiceDashboard() {
        setupPaymentModal();
    }

    function setupPaymentModal() {
        // Configure payment button events
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('pay-invoice-btn') || 
                e.target.closest('.pay-invoice-btn')) {
                
                e.preventDefault();
                const btn = e.target.classList.contains('pay-invoice-btn') 
                    ? e.target 
                    : e.target.closest('.pay-invoice-btn');
                
                const invoiceId = btn.dataset.invoiceId;
                const amount = btn.dataset.amount;
                const invoiceName = btn.dataset.invoiceName;
                
                openPaymentModal(invoiceId, amount, invoiceName);
            }
        });

        // Configure save payment button
        const savePaymentBtn = document.getElementById('savePayment');
        if (savePaymentBtn) {
            savePaymentBtn.addEventListener('click', function() {
                savePayment();
            });
        }
    }

    function openPaymentModal(invoiceId, amount, invoiceName) {
        // Fill form with invoice data
        document.getElementById('invoice_id').value = invoiceId;
        document.getElementById('invoice_name').value = invoiceName;
        document.getElementById('amount').value = amount;
        
        // Set current date as default
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('payment_date').value = today;
        
        // Show modal (using Bootstrap)
        const modal = document.getElementById('paymentModal');
        if (window.$ && window.$.fn.modal) {
            window.$(modal).modal('show');
        } else {
            // Fallback for showing modal without jQuery/Bootstrap
            modal.style.display = 'block';
            modal.classList.add('show');
            document.body.classList.add('modal-open');
        }
    }

    function savePayment() {
        const form = document.getElementById('paymentForm');
        const formData = new FormData(form);
        
        const paymentData = {
            factura_id: parseInt(formData.get('invoice_id')),
            monto: parseFloat(formData.get('amount')),
            metodo_pago: formData.get('payment_method'),
            fecha_pago: formData.get('payment_date'),
            referencia: formData.get('reference'),
            observaciones: formData.get('observations')
        };

        // Make AJAX request to save payment
        fetch('/custom_clients/register_payment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify(paymentData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Show success message
                showNotification('Pago registrado exitosamente', 'success');
                
                // Close modal
                closePaymentModal();
                
                // Reload page to reflect changes
                window.location.reload();
                
                // Clear form
                form.reset();
            } else {
                showNotification('Error al registrar el pago: ' + data.message, 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error al registrar el pago', 'danger');
        });
    }

    function closePaymentModal() {
        const modal = document.getElementById('paymentModal');
        if (window.$ && window.$.fn.modal) {
            window.$(modal).modal('hide');
        } else {
            modal.style.display = 'none';
            modal.classList.remove('show');
            document.body.classList.remove('modal-open');
        }
    }

    function showNotification(message, type) {
        // Simple notification system
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show`;
        notification.style.position = 'fixed';
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.zIndex = '9999';
        notification.innerHTML = `
            ${message}
            <button type="button" class="close" onclick="this.parentElement.remove();">
                <span>&times;</span>
            </button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

})();
