from odoo import models, fields

class InternetPlan(models.Model):
    _name = 'internet.plan'
    _description = 'Plan de Internet'

    name = fields.Char('Nombre del Plan', required=True)
    upload_speed = fields.Float('Velocidad subida (Mbps)', required=True)
    download_speed = fields.Float('Velocidad bajada (Mbps)', required=True)
    price = fields.Float('Precio Mensual (Bs)', required=True)
    description = fields.Text('Descripción')
    active = fields.Boolean('Plan activo', default=True)

    def name_get(self):
        return [(rec.id, f"{rec.name} ({rec.download_speed} Mbps)") for rec in self]
