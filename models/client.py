from odoo import models, fields

class Client(models.Model):
    _name = "custom.client"
    _description = "Cliente personalizado"

    name = fields.Char(string="Nombre", required=True)
    nit = fields.Char(string="NIT", required=True)
    email = fields.Char(string="Correo electrónico")
    phone = fields.Char(string="Teléfono")
    active = fields.Boolean(string="Activo", default=True)
