from odoo import models, fields, api
from datetime import date

class InternetInvoice(models.Model):
    _name = 'internet.invoice'
    _description = 'Factura mensual del cliente'
    _rec_name = 'name'
    _order = 'date_invoice desc'

    name = fields.Char('Número', required=True, copy=False, readonly=True, default='New')
    
    # Campos según el diagrama
    contrato_id = fields.Many2one('internet.contract', string='Contrato', required=True, ondelete='cascade')
    fecha_factura = fields.Date('Fecha de Factura', default=fields.Date.context_today, required=True)
    fecha_vencimiento = fields.Date('Fecha de Vencimiento', required=True)
    monto_factura = fields.Float('Monto Factura', digits=(16,2), required=True)
    monto_pagado = fields.Float('Monto Pagado', digits=(16,2), compute='_compute_monto_pagado', store=True)
    saldo_pendiente = fields.Float('Saldo Pendiente', digits=(16,2), compute='_compute_saldo_pendiente', store=True)
    estado = fields.Selection([
        ('pagada', 'Pagada'), 
        ('impaga', 'Impaga'),
        ('parcial', 'Pago Parcial'),
        ('vencida', 'Vencida'),
    ], string='Estado', default='impaga', required=True)
    
    # Campos anteriores mantenidos para compatibilidad
    client_id = fields.Many2one('internet.client', string='Cliente (Legacy)', compute='_compute_client_id', store=True)
    date_invoice = fields.Date('Fecha de emisión', default=fields.Date.context_today)
    due_date = fields.Date('Fecha de vencimiento')
    amount = fields.Float('Monto', digits=(16,2))
    state = fields.Selection([('pagada','Pagada'), ('impaga','Impaga')], string='Estado (Legacy)', default='impaga')
    
    # Relaciones según el diagrama
    pago_ids = fields.One2many('internet.pagos', 'factura_id', string='Pagos')
    aviso_cobro_ids = fields.One2many('internet.aviso_cobro', 'factura_id', string='Avisos de Cobro')
    
    @api.depends('contrato_id')
    def _compute_client_id(self):
        for record in self:
            record.client_id = record.contrato_id.cliente_id if record.contrato_id else False
    
    @api.depends('pago_ids.monto')
    def _compute_monto_pagado(self):
        for record in self:
            record.monto_pagado = sum(record.pago_ids.mapped('monto'))
    
    @api.depends('monto_factura', 'monto_pagado')
    def _compute_saldo_pendiente(self):
        for record in self:
            record.saldo_pendiente = record.monto_factura - record.monto_pagado
            # Actualizar estado según el saldo
            if record.saldo_pendiente <= 0:
                record.estado = 'pagada'
            elif record.monto_pagado > 0:
                record.estado = 'parcial'
            elif record.fecha_vencimiento and record.fecha_vencimiento < fields.Date.context_today(record):
                record.estado = 'vencida'
            else:
                record.estado = 'impaga'

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('internet.invoice') or '/'
        
        # Sincronizar campos nuevos con legacy
        if 'contrato_id' in vals and vals.get('contrato_id'):
            contrato = self.env['internet.contract'].browse(vals['contrato_id'])
            if contrato.plan_id and not vals.get('monto_factura'):
                vals['monto_factura'] = contrato.plan_id.price
                vals['amount'] = contrato.plan_id.price
                
        if not vals.get('due_date') and not vals.get('fecha_vencimiento'):
            vals['due_date'] = date.today()
            vals['fecha_vencimiento'] = date.today()
            
        if vals.get('fecha_factura') and not vals.get('date_invoice'):
            vals['date_invoice'] = vals['fecha_factura']
            
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

