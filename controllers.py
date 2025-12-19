from odoo import http
from odoo.http import request
import json

class CustomInvoiceDashboard(http.Controller):
    @http.route('/custom_clients/invoice_dashboard', auth='user', website=True)
    def invoice_dashboard(self, **kw):
        """Renderizar dashboard de facturas agrupadas por cliente"""
        invoice_model = request.env['internet.invoice']
        dashboard_data = invoice_model.get_dashboard_data()
        
        return request.render('custom_clients.custom_clients.invoice_dashboard_template', dashboard_data)
    
    @http.route('/custom_clients/register_payment', type='json', auth='user', methods=['POST'])
    def register_payment(self, **kw):
        """Endpoint para registrar pagos vía AJAX"""
        try:
            payment_data = {
                'factura_id': kw.get('factura_id'),
                'monto': float(kw.get('monto', 0)),
                'metodo_pago': kw.get('metodo_pago'),
                'fecha_pago': kw.get('fecha_pago'),
                'referencia': kw.get('referencia'),
                'observaciones': kw.get('observaciones')
            }
            
            # Crear el pago
            payment = request.env['internet.pagos'].create(payment_data)
            
            # Recalcular estado de la factura
            invoice = request.env['internet.invoice'].browse(payment_data['factura_id'])
            invoice._compute_saldo_pendiente()
            
            # Actualizar estado según el saldo
            if invoice.saldo_pendiente <= 0:
                invoice.estado = 'pagada'
            elif invoice.saldo_pendiente < invoice.monto_factura:
                invoice.estado = 'parcial'
            
            return {
                'success': True,
                'message': 'Pago registrado exitosamente',
                'payment_id': payment.id
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al registrar el pago: {str(e)}'
            }
