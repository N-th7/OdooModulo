from odoo import models, fields, api

class InternetClient(models.Model):
    _name = 'internet.client'
    _description = 'Cliente de Internet'
    _rec_name = 'name'

    id = fields.Char('ID Cliente', readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('internet.client'))
    name = fields.Char('Nombre(s)', required=True)
    second_name = fields.Char('Apellido(s)', required=True)
    social_reason = fields.Char('Razón Social')
    client_type = fields.Selection([
        ('residencial', 'Residencial'),
        ('empresa', 'Empresa'),
    ], string='Tipo de Cliente', default='residencial', required=True)
    ci = fields.Char('CI / NIT', required=True)
    phone = fields.Char('Teléfono', required=True)
    alternative_phone = fields.Char('Teléfono alternativo')
    email = fields.Char('Correo electrónico')
    active = fields.Boolean('Activo', default=True)
    seller_id = fields.Many2one('res.users', string='Vendedor', default=lambda self: self.env.user)
    city = fields.Selection([
        ('la_paz', 'La Paz'),
        ('el_alto', 'El Alto'),
        ('cochabamba', 'Cochabamba'),
        ('santa_cruz', 'Santa Cruz'),
        ('oruro', 'Oruro'),
        ('potosi', 'Potosí'),
        ('sucre', 'Sucre'),
        ('tarija', 'Tarija'),
        ('beni', 'Beni'),
        ('pando', 'Pando'),
    ], string='Ciudad', required=True)

    observations = fields.Text('Observaciones')
    registration_date = fields.Date('Fecha de registro', default=fields.Date.context_today)
    contract_ids = fields.One2many(
    'internet.contract',  
    'client_id',          
    string='Contratos'
)
    

    invoice_ids = fields.One2many('internet.invoice', 'client_id', string='Facturas')

    deuda_meses = fields.Integer('Meses adeudados', compute='_compute_deuda', store=True)

    @api.depends('invoice_ids.state')
    def _compute_deuda(self):
        for rec in self:
            impagas = rec.invoice_ids.filtered(lambda i: i.state == 'impaga')
            rec.deuda_meses = len(impagas)

    def action_apply_cut(self):
        """Acción para aplicar corte manual o desde cron"""
        for rec in self:
            if rec.deuda_meses >= 2:
                rec.status = 'cortado'
            elif rec.deuda_meses > 0:
                rec.status = 'suspendido'
            else:
                rec.status = 'activo'

    def action_reconnect(self):
        """Reactivar servicio (por pago o gestión)"""
        for rec in self:
            rec.status = 'activo'

    @api.model
    def _cron_check_clients_for_cut(self):
        """Buscar clientes con 2 o más facturas impagas y aplicar corte."""
        clients = self.search([('active', '=', True)])
        for client in clients:
            # recomputa deuda_meses automáticamente si 'store' y @depends están bien
            client._compute_deuda()
            if client.deuda_meses >= 2 and client.status != 'cortado':
                client.status = 'cortado'
            elif client.deuda_meses == 1 and client.status == 'activo':
                client.status = 'suspendido'
                

def action_new_contract(self):
    self.ensure_one()
    return {
        'name': "Nuevo Contrato",
        'view_mode': 'form',
        'res_model': 'internet.contract',
        'type': 'ir.actions.act_window',
        'context': {
            'default_client_id': self.id
        },
        'target': 'new',  # modal popup
    }

