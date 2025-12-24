from odoo import models, fields, api

class Instalacion(models.Model):
    _name = 'internet.instalacion'
    _description = 'Instalación de Internet'

    puerto_id = fields.Many2one('internet.puerto', string='Puerto')
    contrato_id = fields.Many2one('internet.contract', string='Contrato', required=True)
    fecha_instalacion = fields.Date('Fecha de Instalación')
    estado = fields.Selection([
        ('programada', 'Programada'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ], string='Estado', default='programada', required=True)
    fecha_baja = fields.Date('Fecha de Baja')
    nota = fields.Text('Nota')
    empresa_instaladora = fields.Char('Empresa Instaladora')

    equipo_extra_ids = fields.One2many('internet.equipo_extra', 'instalacion_id', string='Equipos Extra')
    onu_ids = fields.One2many('internet.onu', 'instalacion_id', string='ONUs')
    rango_ip_ids = fields.One2many('internet.rango_ip', 'instalacion_id', string='Rangos IP')

    name = fields.Char('Nombre', compute='_compute_name', store=True)

    @api.depends('contrato_id', 'fecha_instalacion')
    def _compute_name(self):
        for record in self:
            if record.contrato_id and record.fecha_instalacion:
                record.name = f"Instalación {record.contrato_id.name} - {record.fecha_instalacion}"
            else:
                record.name = f"Instalación {record.id or 'Nueva'}"