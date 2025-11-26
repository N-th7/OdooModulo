from odoo import models, fields, api

class InternetContract(models.Model):
    _name = "internet.contract"
    _description = "Contrato de Internet"

    code = fields.Char(string="Código", readonly=True, copy=False, default='New')

    client_id = fields.Many2one('internet.client', string='Cliente', ondelete='cascade')
    plan_id = fields.Many2one('internet.plan', string='Plan de Internet', required=True, placeholder='Seleccione un plan')
    start_date = fields.Date('Fecha de Inicio', required=True)

    contract_type = fields.Selection(  [
        ('mensual', 'Mensual'),
        ('anual', 'Anual'),
    ], default='mensual' string='Tipo de Contrato',  placeholder='Seleccione el tipo de contrato' )

    address = fields.Char(string='Dirección', required=True, placeholder='Calle, número, ciudad')
    zone = fields.Char(string='Zona', placeholder='Zona o barrio', required=True)
    gps = fields.Char( string='Coordenadas GPS', placeholder='Latitud, Longitud' )
    reference = fields.Char( string='Referencia', placeholder='Puntos de referencia cercanos' )
    url_location = fields.Char( string='URL de Ubicación', placeholder='Enlace a Google Maps' )
    requires_invoice = fields.Boolean( string='Requiere Factura', default=False )
    observations = fields.Text( string='Observaciones')
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
