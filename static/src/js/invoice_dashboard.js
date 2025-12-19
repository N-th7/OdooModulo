/** @odoo-module */

import { registry } from "@web/core/registry";
import { Component, useState, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class InvoiceDashboard extends Component {
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
        // Configurar eventos para los botones de pago
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('pay-invoice-btn') || 
                e.target.closest('.pay-invoice-btn')) {
                
                const btn = e.target.classList.contains('pay-invoice-btn') 
                    ? e.target 
                    : e.target.closest('.pay-invoice-btn');
                
                const invoiceId = btn.dataset.invoiceId;
                const amount = btn.dataset.amount;
                const invoiceName = btn.dataset.invoiceName;
                
                this.openPaymentModal(invoiceId, amount, invoiceName);
            }
        });

        // Configurar evento para guardar pago
        const savePaymentBtn = document.getElementById('savePayment');
        if (savePaymentBtn) {
            savePaymentBtn.addEventListener('click', () => {
                this.savePayment();
            });
        }
    }

    openPaymentModal(invoiceId, amount, invoiceName) {
        // Llenar el formulario con los datos de la factura
        document.getElementById('invoice_id').value = invoiceId;
        document.getElementById('invoice_name').value = invoiceName;
        document.getElementById('amount').value = amount;
        
        // Establecer fecha actual por defecto
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('payment_date').value = today;
        
        // Mostrar modal (usando Bootstrap)
        const modal = document.getElementById('paymentModal');
        if (window.$ && window.$.fn.modal) {
            window.$(modal).modal('show');
        } else {
            // Fallback para mostrar modal sin jQuery/Bootstrap
            modal.style.display = 'block';
            modal.classList.add('show');
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

            // Cerrar modal
            const modal = document.getElementById('paymentModal');
            if (window.$ && window.$.fn.modal) {
                window.$(modal).modal('hide');
            } else {
                modal.style.display = 'none';
                modal.classList.remove('show');
            }

            // Recargar datos del dashboard
            this.loadDashboardData();
            
            // Limpiar formulario
            form.reset();

        } catch (error) {
            console.error("Error saving payment:", error);
            this.notification.add("Error al registrar el pago", {
                type: "danger"
            });
        }
    }
}

registry.category("actions").add("custom_invoice_dashboard", InvoiceDashboard);
