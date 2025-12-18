from odoo import models, fields, api

class RangoIP(models.Model):
    _name = 'internet.rango_ip'
    _description = 'Rango IP'

    # Campos según el diagrama
    instalacion_id = fields.Many2one('internet.instalacion', string='Instalación', required=True)
    lan = fields.Char('LAN', required=True)
    wan = fields.Char('WAN', required=True)

    # Campo relacional
    contrato_id = fields.Many2one(related='instalacion_id.contrato_id', string='Contrato', store=True)

    name = fields.Char('Nombre', compute='_compute_name', store=True)

    @api.depends('lan', 'wan', 'instalacion_id')
    def _compute_name(self):
        for record in self:
            record.name = f"IP {record.lan}/{record.wan} - {record.instalacion_id.contrato_id.name if record.instalacion_id and record.instalacion_id.contrato_id else 'Sin contrato'}"