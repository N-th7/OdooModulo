from odoo import models, fields

class InternetPlan(models.Model):
    _name = 'internet.plan'
    _description = 'Plan de Internet'

    name = fields.Char('Nombre del plan', required=True)
    speed = fields.Char('Velocidad')
    price = fields.Float('Precio mensual', required=True, digits=(16,2))
    description = fields.Text('Descripción')
