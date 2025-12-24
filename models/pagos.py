from odoo import models, fields, api

class Pagos(models.Model):
    _name = 'internet.pagos'
    _description = 'Pagos de Facturas'
    _order = 'fecha_pago desc'

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
        if pago.factura_id:
            factura = pago.factura_id
            factura._compute_saldo_pendiente()
            
            if factura.saldo_pendiente <= 0:
                factura.estado = 'pagada'
            elif factura.saldo_pendiente < factura.monto_factura:
                factura.estado = 'parcial'
            else:
                if factura.fecha_vencimiento < factura.fecha_factura.today():
                    factura.estado = 'vencida'
                else:
                    factura.estado = 'impaga'
        
        return pago
    
    def write(self, vals):
        res = super().write(vals)
        for pago in self:
            if pago.factura_id:
                factura = pago.factura_id
                factura._compute_saldo_pendiente()
                
                if factura.saldo_pendiente <= 0:
                    factura.estado = 'pagada'
                elif factura.saldo_pendiente < factura.monto_factura:
                    factura.estado = 'parcial'
                else:
                    if factura.fecha_vencimiento < factura.fecha_factura.today():
                        factura.estado = 'vencida'
                    else:
                        factura.estado = 'impaga'
        return res
    
    def unlink(self):
        facturas = self.mapped('factura_id')
        res = super().unlink()
        for factura in facturas:
            if factura.exists():
                factura._compute_saldo_pendiente()
                
                if factura.saldo_pendiente <= 0:
                    factura.estado = 'pagada'
                elif factura.saldo_pendiente < factura.monto_factura:
                    factura.estado = 'parcial'
                else:
                    if factura.fecha_vencimiento < factura.fecha_factura.today():
                        factura.estado = 'vencida'
                    else:
                        factura.estado = 'impaga'
        return res