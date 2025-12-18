from odoo import models, fields, api

class Pagos(models.Model):
    _name = 'internet.pagos'
    _description = 'Pagos de Facturas'
    _order = 'fecha_pago desc'

    # Campos según el diagrama
    factura_id = fields.Many2one('internet.invoice', string='Factura', required=True)
    fecha_pago = fields.Date('Fecha de Pago', required=True, default=fields.Date.context_today)
    monto = fields.Float('Monto', required=True)
    metodo_pago = fields.Selection([
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('deposito', 'Depósito'),
        ('qr', 'QR'),
        ('tarjeta', 'Tarjeta'),
    ], string='Método de Pago', required=True)
    referencia = fields.Char('Referencia')
    observaciones = fields.Text('Observaciones')

    # Campos computados y relacionales
    cliente_id = fields.Many2one(related='factura_id.client_id', string='Cliente', store=True)
    contrato_id = fields.Many2one(related='factura_id.contrato_id', string='Contrato', store=True)

    name = fields.Char('Nombre', compute='_compute_name', store=True)

    @api.depends('factura_id', 'fecha_pago', 'monto')
    def _compute_name(self):
        for record in self:
            if record.factura_id:
                record.name = f"Pago {record.factura_id.name} - Bs. {record.monto}"
            else:
                record.name = f"Pago {record.id or 'Nuevo'}"

    @api.model
    def create(self, vals):
        pago = super().create(vals)
        # Actualizar el saldo de la factura cuando se registre un pago
        if pago.factura_id:
            pago.factura_id._compute_saldo_pendiente()
        return pago