from odoo import models, fields, api

class EquipoExtra(models.Model):
    _name = 'internet.equipo_extra'
    _description = 'Equipo Extra'

    instalacion_id = fields.Many2one('internet.instalacion', string='Instalación', required=True)
    numero_equipo = fields.Char('Número de Equipo', required=True)
    tipo = fields.Selection([
        ('router', 'Router'),
        ('switch', 'Switch'),
        ('access_point', 'Access Point'),
        ('repetidor', 'Repetidor'),
        ('otros', 'Otros'),
    ], string='Tipo', required=True)
    marca = fields.Char('Marca')
    modelo = fields.Char('Modelo')
    serial_number = fields.Char('Número de Serie')
    observaciones = fields.Text('Observaciones')
    usuario = fields.Char('Usuario')
    contraseña = fields.Char('Contraseña')

    contrato_id = fields.Many2one(related='instalacion_id.contrato_id', string='Contrato', store=True)

    name = fields.Char('Nombre', compute='_compute_name', store=True)

    @api.depends('tipo', 'numero_equipo')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.tipo.title() if record.tipo else 'Equipo'} - {record.numero_equipo or record.id}"