from odoo import models, fields, api

class InternetContract(models.Model):
    _name = "internet.contract"
    _description = "Contrato de Internet"
    _rec_name = 'code'

    code = fields.Char(string="Código", readonly=True, copy=False, default='New')

    # Campos según el diagrama
    cliente_id = fields.Many2one('internet.client', string='Cliente', required=True, ondelete='cascade')
    plan_id = fields.Many2one('internet.plan', string='Plan', required=True)
    direccion_servicio = fields.Text('Dirección del Servicio', required=True)
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

    # Campos anteriores mantenidos para compatibilidad
    start_date = fields.Date('Fecha de Inicio', required=True)
    end_date = fields.Date('Fecha de Fin')    

    contract_type = fields.Selection([
        ('mensual', 'Mensual'),
        ('anual', 'Anual'),
    ], default='mensual', string='Tipo de Contrato')

    address = fields.Char(string='Dirección', required=True)
    zone = fields.Char(string='Zona', required=True)
    gps = fields.Char(string='Coordenadas GPS')
    reference = fields.Char(string='Referencia')
    url_location = fields.Char(string='URL de Ubicación')
    requires_invoice = fields.Boolean(string='Requiere Factura', default=False)
    observations = fields.Text(string='Observaciones')
    active = fields.Boolean(default=True)

    # Campo de compatibilidad
    client_id = fields.Many2one(related='cliente_id', string='Cliente (Legacy)', store=True, readonly=True)

    # Relaciones según el diagrama
    instalacion_ids = fields.One2many('internet.instalacion', 'contrato_id', string='Instalaciones')
    invoice_ids = fields.One2many('internet.invoice', 'contrato_id', string='Facturas')
    ticket_ids = fields.One2many('internet.tickets', 'contrato_id', string='Tickets')
    aviso_cobro_ids = fields.One2many('internet.aviso_cobro', 'contrato_id', string='Avisos de Cobro')

    # Compatibilidad con nombre anterior  
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
            label = f"{rec.code} {rec.client_id.name} {rec.client_id.second_name}({rec.client_id.ci}) - {rec.plan_id.name}"
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
