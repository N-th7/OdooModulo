from odoo import models, fields, api
from datetime import date, timedelta

class InternetInvoice(models.Model):
    _name = 'internet.invoice'
    _description = 'Factura mensual del cliente'
    _rec_name = 'name'
    _order = 'date_invoice desc'

    name = fields.Char('Número', required=True, copy=False, readonly=True, default='New')
    
    # Campos según el diagrama
    contrato_id = fields.Many2one('internet.contract', string='Contrato')
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
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            # Generar número de factura con formato: [numero de contrato-dia-mes-año-secuencia]
            contract_id = vals.get('contrato_id')
            if contract_id:
                contract = self.env['internet.contract'].browse(contract_id)
                contract_code = contract.code if contract.code != 'New' else 'SIN-CODIGO'
            else:
                contract_code = 'SIN-CONTRATO'
            
            # Obtener fecha actual
            today = fields.Date.context_today(self)
            day = today.strftime('%d')
            month = today.strftime('%m') 
            year = today.strftime('%Y')
            
            # Buscar facturas existentes con el mismo patrón para evitar duplicados
            base_pattern = f"{contract_code}-{day}-{month}-{year}"
            existing_count = self.search_count([
                ('name', 'like', base_pattern + '%')
            ])
            
            # Generar número con secuencia si hay duplicados
            if existing_count > 0:
                vals['name'] = f"{base_pattern}-{existing_count + 1:02d}"
            else:
                vals['name'] = base_pattern
        return super(InternetInvoice, self).create(vals)

    @api.model
    def get_dashboard_data(self):
        """Obtener datos para el dashboard de facturas agrupadas por cliente"""
        # Obtener todas las facturas con sus clientes
        invoices = self.search([])
        
        # Calcular totales generales
        total_invoices = len(invoices)
        total_income = sum(inv.monto_pagado for inv in invoices)
        total_pending = sum(inv.saldo_pendiente for inv in invoices)
        overdue_count = len(invoices.filtered(lambda inv: inv.fecha_vencimiento < fields.Date.today() and inv.saldo_pendiente > 0))
        
        # Agrupar facturas por cliente
        client_groups = {}
        for invoice in invoices:
            client = invoice.client_id
            if not client:
                continue
                
            client_key = client.id
            if client_key not in client_groups:
                client_groups[client_key] = {
                    'client_id': client.id,
                    'client_name': client.nombre_completo or 'Cliente sin nombre',
                    'client_phone': client.phone or 'No registrado',
                    'client_email': client.email or 'No registrado',
                    'invoices': [],
                    'total_pending': 0.0,
                    'total_amount': 0.0
                }
            
            client_groups[client_key]['invoices'].append(invoice)
            client_groups[client_key]['total_pending'] += invoice.saldo_pendiente
            client_groups[client_key]['total_amount'] += invoice.monto_factura
        
        # Convertir a lista y ordenar por deuda pendiente (mayor a menor)
        client_groups_list = list(client_groups.values())
        client_groups_list.sort(key=lambda x: x['total_pending'], reverse=True)
        
        return {
            'total_invoices': total_invoices,
            'total_income': total_income,
            'total_pending': total_pending,
            'overdue_count': overdue_count,
            'client_groups': client_groups_list
        }

    @api.model
    def _cron_generate_invoices(self):
        """Crear una factura por cada contrato activo con el monto del plan, cada 18 del mes."""
        # Buscar contratos activos
        contracts = self.env['internet.contract'].search([
            ('estado', '=', 'activo'),
            ('cliente_id', '!=', False),
            ('plan_id', '!=', False)
        ])
        
        today = fields.Date.context_today(self)
        
        # Solo generar facturas si es día 18
        if today.day != 18:
            return
            
        for contract in contracts:
            # Verificar si ya existe factura para este contrato este mes
            existing_invoice = self.search([
                ('contrato_id', '=', contract.id),
                ('fecha_factura', '>=', today.replace(day=1)),  # Desde el 1ro del mes
                ('fecha_factura', '<=', today)  # Hasta hoy
            ], limit=1)
            
            if existing_invoice:
                continue
                
            # Calcular fecha de vencimiento (30 días después)
            due_date = today + timedelta(days=30)
            
            # Crear factura con monto del plan
            plan_amount = contract.plan_id.price if contract.plan_id else 0.0
            
            self.create({
                'contrato_id': contract.id,
                'fecha_factura': today,
                'fecha_vencimiento': due_date,
                'monto_factura': plan_amount,
                'estado': 'impaga'
            })

