from odoo import models, fields, api

class InternetContract(models.Model):
    _name = "internet.contract"
    _description = "Contrato de Internet"

    code = fields.Char(string="Código", readonly=True, copy=False, default='New')

    client_id = fields.Many2one('internet.client', string='Cliente', ondelete='cascade')
    plan_id = fields.Many2one('internet.plan', string='Plan de Internet', required=True)
    start_date = fields.Date('Fecha de Inicio', required=True)

    contract_type = fields.Selection([
        ('mensual', 'Mensual'),
        ('anual', 'Anual'),
    ], default='mensual')

    address = fields.Char()
    zone = fields.Char()
    gps = fields.Char()
    reference = fields.Char()
    url_location = fields.Char()
    requires_invoice = fields.Boolean()
    observations = fields.Text()
    active = fields.Boolean(default=True)

    state = fields.Selection([
        ('activo', 'Activo'),
        ('suspendido', 'Suspendido'),
        ('cancelado', 'Cancelado'),
    ], default='activo')

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('internet.contract') or 'New'
        return super().create(vals)
