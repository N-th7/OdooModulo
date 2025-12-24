from odoo import models, fields, api

class ONU(models.Model):
    _name = 'internet.onu'
    _description = 'ONU (Optical Network Unit)'

    instalacion_id = fields.Many2one('internet.instalacion', string='Instalación', required=True)
    marca = fields.Char('Marca', required=True)
    modelo = fields.Char('Modelo', required=True)
    pot_up = fields.Float('Potencia Subida (dBm)')
    wifi_ssid = fields.Char('WiFi SSID')
    wifi_password = fields.Char('WiFi Password')
    observaciones = fields.Text('Observaciones')

    contrato_id = fields.Many2one(related='instalacion_id.contrato_id', string='Contrato', store=True)

    name = fields.Char('Nombre', compute='_compute_name', store=True)

    @api.depends('marca', 'modelo', 'instalacion_id')
    def _compute_name(self):
        for record in self:
            record.name = f"ONU {record.marca} {record.modelo} - {record.instalacion_id.contrato_id.name if record.instalacion_id and record.instalacion_id.contrato_id else 'Sin contrato'}"