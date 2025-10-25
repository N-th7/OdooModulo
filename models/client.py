from odoo import models, fields, api

class InternetClient(models.Model):
    _name = 'internet.client'
    _description = 'Cliente de Internet'
    _rec_name = 'name'

    name = fields.Char('Nombre completo', required=True)
    ci = fields.Char('CI / NIT')
    address = fields.Char('Dirección')
    phone = fields.Char('Teléfono')
    email = fields.Char('Correo electrónico')
    plan_id = fields.Many2one('internet.plan', string='Plan contratado', required=True)
    active = fields.Boolean('Activo', default=True)
    status = fields.Selection([
        ('activo', 'Activo'),
        ('suspendido', 'Suspendido'),
        ('cortado', 'Cortado'),
    ], string='Estado del servicio', default='activo')

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
