/** @odoo-module */

import { registry } from "@web/core/registry";
import { Component, useState, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class InvoiceDashboardAction extends Component {
    static template = "custom_clients.invoice_dashboard_template";

    setup() {
        this.rpc = useService("rpc");
        this.notification = useService("notification");
        this.state = useState({
            dashboardData: null,
            loading: true
        });

        onMounted(() => {
            this.loadDashboardData();
            this.setupPaymentModal();
        });
    }

    async loadDashboardData() {
        try {
            const data = await this.rpc("/web/dataset/call_kw", {
                model: "internet.invoice",
                method: "get_dashboard_data",
                args: [],
                kwargs: {}
            });
            this.state.dashboardData = data;
            this.state.loading = false;
        } catch (error) {
            console.error("Error loading dashboard data:", error);
            this.state.loading = false;
        }
    }

    setupPaymentModal() {
        setTimeout(() => {
            this.setupPaymentEvents();
            this.setupToggleEvents();
        }, 100);
    }

    setupPaymentEvents() {
        const container = document.querySelector('.o_invoice_container');
        if (!container) return;

        container.addEventListener('click', (e) => {
            if (e.target.classList.contains('pay-invoice-btn') || 
                e.target.closest('.pay-invoice-btn')) {
                
                e.preventDefault();
                const btn = e.target.classList.contains('pay-invoice-btn') 
                    ? e.target 
                    : e.target.closest('.pay-invoice-btn');
                
                const invoiceId = btn.dataset.invoiceId;
                const amount = btn.dataset.amount;
                const invoiceName = btn.dataset.invoiceName;
                
                this.openPaymentModal(invoiceId, amount, invoiceName);
            }
        });

        const savePaymentBtn = document.getElementById('savePayment');
        if (savePaymentBtn) {
            savePaymentBtn.addEventListener('click', () => {
                this.savePayment();
            });
        }
    }

    setupToggleEvents() {
        const container = document.querySelector('.o_invoice_container');
        if (!container) return;

        container.addEventListener('click', (e) => {
            const header = e.target.closest('.o_client_header');
            if (header) {
                e.preventDefault();
                const clientId = header.dataset.clientId;
                this.toggleClientGroup(clientId);
            }
        });
    }

    toggleClientGroup(clientId) {
        const invoicesList = document.getElementById(`invoices-${clientId}`);
        const toggleIcon = document.getElementById(`toggle-icon-${clientId}`);
        
        if (!invoicesList || !toggleIcon) return;

        if (invoicesList.style.display === 'none') {
            invoicesList.style.display = 'block';
            toggleIcon.classList.remove('fa-chevron-right');
            toggleIcon.classList.add('fa-chevron-down');
            toggleIcon.classList.add('expanded');
        } else {
            invoicesList.style.display = 'none';
            toggleIcon.classList.remove('fa-chevron-down');
            toggleIcon.classList.add('fa-chevron-right');
            toggleIcon.classList.remove('expanded');
        }
    }

    openPaymentModal(invoiceId, amount, invoiceName) {
        document.getElementById('invoice_id').value = invoiceId;
        document.getElementById('invoice_name').value = invoiceName;
        document.getElementById('amount').value = amount;
        
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('payment_date').value = today;
        
        const modal = document.getElementById('paymentModal');
        if (window.$ && window.$.fn.modal) {
            window.$(modal).modal('show');
        }
    }

    async savePayment() {
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

        try {
            await this.rpc("/web/dataset/call_kw", {
                model: "internet.pagos",
                method: "create",
                args: [paymentData],
                kwargs: {}
            });

            this.notification.add("Pago registrado exitosamente", {
                type: "success"
            });

            const modal = document.getElementById('paymentModal');
            if (window.$ && window.$.fn.modal) {
                window.$(modal).modal('hide');
            }

            this.loadDashboardData();
            
            form.reset();

        } catch (error) {
            console.error("Error saving payment:", error);
            this.notification.add("Error al registrar el pago", {
                type: "danger"
            });
        }
    }
}

registry.category("actions").add("invoice_dashboard_action", InvoiceDashboardAction);
