from odoo import http
from odoo.http import request

class CustomInvoiceDashboard(http.Controller):
    @http.route('/custom_clients/invoice_dashboard', auth='user', website=True)
    def invoice_dashboard(self, **kw):
        invoices = request.env['internet.invoice'].search([])
        clients = request.env['internet.client'].search([])
        # Agrupar facturas por cliente
        invoices_grouped = {}
        for client in clients:
            invoices_grouped[client] = invoices.filtered(lambda inv: inv.client_id.id == client.id)
        return request.render('custom_clients.custom_invoice_dashboard', {
            'invoices_grouped': invoices_grouped
        })
