from odoo import models, fields,api

class InternetContract(models.Model):
    _name = "internet.contract"
    _description = "Contrato de Internet"

    client_id = fields.Many2one(
        'internet.client',
        string='Cliente',
        ondelete='cascade'
    )

    plan_id = fields.Many2one(
        'internet.plan',
        string='Plan de Internet',
        required=True
    )

    start_date = fields.Date('Fecha de Inicio', required=True)
    contract_type = fields.Selection([
        ('mensual', 'Mensual'),
        ('anual', 'Anual'),
    ], string='Tipo de Contrato', default='mensual')

    address = fields.Char("Dirección del Servicio")
    zone = fields.Char("Zona")
    gps = fields.Char("Coordenadas GPS")
    reference = fields.Char("Referencia de Dirección")
    url_location = fields.Char("URL de Ubicación")
    requires_invoice = fields.Boolean("Cliente requiere factura")
    observations = fields.Text("Observaciones del Contrato")
    active = fields.Boolean('Activo', default=True)
    state = fields.Selection([
    ('activo', 'Activo'),
    ('suspendido', 'Suspendido'),
    ('cancelado', 'Cancelado'),
], string='Estado', default='activo')

    
    def action_activate(self):
        self.write({'state': 'activo'})

    def action_suspend(self):
        self.write({'state': 'suspendido'})

    def action_cancel(self):
        self.write({'state': 'cancelado'})