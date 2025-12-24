from odoo import models, fields, api

class AvisoCobro(models.Model):
    _name = 'internet.aviso_cobro'
    _description = 'Aviso de Cobro'
    _order = 'fecha_aviso desc'

    contrato_id = fields.Many2one('internet.contract', string='Contrato', required=True)
    factura_id = fields.Many2one('internet.invoice', string='Factura', required=True)
    fecha_aviso = fields.Datetime('Fecha de Aviso', default=fields.Datetime.now, required=True)
    medio_envio = fields.Selection([
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('llamada', 'Llamada'),
        ('presencial', 'Presencial'),
    ], string='Medio de Envío', required=True)
    mensaje = fields.Text('Mensaje')
    estado = fields.Selection([
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('leido', 'Leído'),
        ('fallido', 'Fallido'),
    ], string='Estado', default='enviado', required=True)

    cliente_id = fields.Many2one(related='contrato_id.client_id', string='Cliente', store=True)

    name = fields.Char('Nombre', compute='_compute_name', store=True)

    @api.depends('factura_id', 'fecha_aviso', 'medio_envio')
    def _compute_name(self):
        for record in self:
            if record.factura_id:
                record.name = f"Aviso {record.factura_id.name} - {record.medio_envio.title()}"
            else:
                record.name = f"Aviso {record.id or 'Nuevo'}"