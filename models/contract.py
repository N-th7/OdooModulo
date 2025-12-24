from odoo import models, fields, api

class InternetContract(models.Model):
    _name = "internet.contract"
    _description = "Contrato de Internet"
    _rec_name = 'code'

    code = fields.Char(string="Código", readonly=True, copy=False, default='New')

    cliente_id = fields.Many2one('internet.client', string='Cliente')
    plan_id = fields.Many2one('internet.plan', string='Plan', required=True)
    direccion_servicio = fields.Text('Dirección del Servicio')
    fecha_activacion = fields.Date('Fecha de Activación')
    fecha_instalacion_programada = fields.Date('Fecha Instalación Programada')
    estado = fields.Selection([
        ('activo', 'Activo'),
        ('suspendido', 'Suspendido'),
        ('cancelado', 'Cancelado'),
        ('pendiente', 'Pendiente'),
    ], string='Estado', default='pendiente', required=True)
    url_ubicacion = fields.Char('URL de Ubicación')
    coordenadas = fields.Char('Coordenadas')

    start_date = fields.Date('Fecha de Inicio', required=True)
    end_date = fields.Date('Fecha de Fin')    

    contract_type = fields.Selection([
        ('mensual', 'Mensual'),
        ('anual', 'Anual'),
    ], default='mensual', string='Tipo de Contrato')

    address = fields.Char(string='Dirección')
    zone = fields.Char(string='Zona')
    gps = fields.Char(string='Coordenadas GPS')
    reference = fields.Char(string='Referencia')
    url_location = fields.Char(string='URL de Ubicación')
    requires_invoice = fields.Boolean(string='Requiere Factura', default=False)
    observations = fields.Text(string='Observaciones')
    active = fields.Boolean(default=True)

    client_id = fields.Many2one(related='cliente_id', string='Cliente (Legacy)', store=True, readonly=True)

    instalacion_ids = fields.One2many('internet.instalacion', 'contrato_id', string='Instalaciones')
    invoice_ids = fields.One2many('internet.invoice', 'contrato_id', string='Facturas')
    ticket_ids = fields.One2many('internet.tickets', 'contrato_id', string='Tickets')
    aviso_cobro_ids = fields.One2many('internet.aviso_cobro', 'contrato_id', string='Avisos de Cobro')

    state = fields.Selection([
        ('activo', 'Activo'),
        ('suspendido', 'Suspendido'),
        ('cancelado', 'Cancelado'),
        ('pendiente', 'Pendiente'),
    ], default='pendiente')

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('internet.contract') or 'New'
        return super().create(vals)

    def name_get(self):
        result = []
        for rec in self:
            client_name = ''
            if rec.cliente_id:
                client_name = f"{rec.cliente_id.name or ''} {rec.cliente_id.second_name or ''}({rec.cliente_id.ci or ''})".strip()
            plan_name = rec.plan_id.name if rec.plan_id else 'Sin Plan'
            label = f"{rec.code} {client_name} - {plan_name}"
            result.append((rec.id, label))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if not name:
            recs = self.search(args, limit=limit)
            return recs.name_get()

        domain = [
            '|', '|', '|',
            ('code', operator, name),
            ('start_date', operator, name),
            ('state', operator, name),
        ]

        recs = self.search(domain + args, limit=limit)
        return recs.name_get()
