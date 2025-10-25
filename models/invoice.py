from odoo import models, fields, api
from datetime import date

class InternetInvoice(models.Model):
    _name = 'internet.invoice'
    _description = 'Factura mensual del cliente'
    _rec_name = 'name'
    _order = 'date_invoice desc'

    name = fields.Char('Número', required=True, copy=False, readonly=True, default='New')
    client_id = fields.Many2one('internet.client', string='Cliente', required=True, ondelete='cascade')
    date_invoice = fields.Date('Fecha de emisión', default=fields.Date.context_today)
    due_date = fields.Date('Fecha de vencimiento')
    amount = fields.Float('Monto', digits=(16,2))
    state = fields.Selection([('pagada','Pagada'), ('impaga','Impaga')], string='Estado', default='impaga')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('internet.invoice') or '/'
        if 'client_id' in vals and not vals.get('amount'):
            client = self.env['internet.client'].browse(vals['client_id'])
            vals['amount'] = client.plan_id.price if client and client.plan_id else 0.0
        if not vals.get('due_date'):
            vals['due_date'] = date.today()
        return super().create(vals)

    def action_register_payment(self):
        for inv in self:
            inv.state = 'pagada'

    @api.model
    def _cron_generate_invoices(self):
        """Crear una factura por cada cliente activo, una vez al mes."""
        clients = self.env['internet.client'].search([('active', '=', True)])
        today = fields.Date.context_today(self)
        for client in clients:
            exists = self.search([
                ('client_id', '=', client.id),
                ('date_invoice', '=', today)
            ], limit=1)
            if exists:
                continue
            self.create({
                'client_id': client.id,
                'date_invoice': today,
                'due_date': today,  
            })

