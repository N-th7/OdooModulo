from odoo import models, fields

class Puerto(models.Model):
    _name = 'internet.puerto'
    _description = 'Puerto de Conexión'

    name = fields.Char('Nombre del Puerto', required=True)
    numero = fields.Char('Número', required=True)
    tipo = fields.Selection([
        ('fibra', 'Fibra Óptica'),
        ('ethernet', 'Ethernet'),
        ('coaxial', 'Coaxial'),
    ], string='Tipo', default='fibra', required=True)
    estado = fields.Selection([
        ('disponible', 'Disponible'),
        ('ocupado', 'Ocupado'),
        ('mantenimiento', 'En Mantenimiento'),
        ('dañado', 'Dañado'),
    ], string='Estado', default='disponible', required=True)
    ubicacion = fields.Char('Ubicación')
    observaciones = fields.Text('Observaciones')

    # Relaciones
    instalacion_ids = fields.One2many('internet.instalacion', 'puerto_id', string='Instalaciones')

    def name_get(self):
        return [(rec.id, f"{rec.name} - {rec.numero}") for rec in self]