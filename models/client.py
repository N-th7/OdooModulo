from odoo import models, fields, api
from odoo.exceptions import ValidationError

class InternetClient(models.Model):
    _name = 'internet.client'
    _description = 'Cliente de Internet'
    _rec_name = 'nombre_completo'  # Use computed field as display name

    _sql_constraints = [
        ('unique_ci', 'unique(ci)', 'El CI / NIT ya está registrado para otro cliente.')
    ]

    # Campos según el diagrama
    cod_cliente = fields.Char('Código de Cliente', required=True, readonly=True, copy=False, default='New')
    nombre_cliente = fields.Char('Nombre Cliente')
    nombre_completo = fields.Char('Nombre Completo', compute='_compute_nombre_completo', store=True)
    numero_telefono = fields.Char('Número Teléfono')
    numero_celular = fields.Char('Número Celular')
    carnet = fields.Char('Carnet')
    # Using 'ci' field from legacy section to avoid duplication
    direccion = fields.Text('Dirección')
    estado = fields.Selection([
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('suspendido', 'Suspendido'),
    ], string='Estado', default='activo', required=True)

    # Campos anteriores mantenidos para compatibilidad
    name = fields.Char('Nombre(s)', required=True)
    second_name = fields.Char('Apellido(s)', required=True)
    social_reason = fields.Char('Razón Social')

    client_type = fields.Selection([
        ('residencial', 'Residencial'),
        ('empresa', 'Empresa'),
    ], string='Tipo de Cliente', default='residencial', required=True)

    ci = fields.Char('CI / NIT', required=True)
    ci_anverso = fields.Binary('Carnet Anverso', attachment=True)
    ci_reverso = fields.Binary('Carnet Reverso', attachment=True)
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

    contract_ids = fields.One2many('internet.contract', 'client_id', string='Contratos')
    contract_count = fields.Integer(string='N° Contratos', compute='_compute_contract_count')
    
    # Nuevas relaciones según el diagrama
    ticket_ids = fields.One2many('internet.tickets', 'cliente_id', string='Tickets')
    ticket_count = fields.Integer(string='N° Tickets', compute='_compute_ticket_count')

    @api.depends('nombre_cliente', 'name', 'second_name')
    def _compute_nombre_completo(self):
        for record in self:
            # Use nombre_cliente first, fallback to name + second_name for compatibility
            if record.nombre_cliente:
                record.nombre_completo = record.nombre_cliente
            else:
                record.nombre_completo = f"{record.name or ''} {record.second_name or ''}".strip()

    @api.depends('ticket_ids')
    def _compute_ticket_count(self):
        for record in self:
            record.ticket_count = len(record.ticket_ids)

    invoice_ids = fields.One2many('internet.invoice', 'client_id', string='Facturas')

    @api.depends('invoice_ids.state')
    def _compute_deuda(self):
        for rec in self:
            rec.deuda_meses = len(rec.invoice_ids.filtered(lambda i: i.state == 'impaga'))

    @api.depends('contract_ids')
    def _compute_contract_count(self):
        for rec in self:
            rec.contract_count = len(rec.contract_ids)


    def action_add_contract(self):
        self.ensure_one()
        return {
            'name': 'Nuevo Contrato',
            'type': 'ir.actions.act_window',
            'res_model': 'internet.contract',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_client_id': self.id},
        }


    def name_get(self):
        result = []
        for rec in self:
            label = f"{rec.name} {rec.second_name} ({rec.ci})"
            result.append((rec.id, label))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []

        if not name:
            return self.search(args, limit=limit).name_get()

        domain = [
            '|', '|', '|', '|',
            ('name', operator, name),
            ('second_name', operator, name),
            ('ci', operator, name),
            ('phone', operator, name),
            ('email', operator, name),
        ]

        recs = self.search(domain + args, limit=limit)
        return recs.name_get()


    @api.constrains('ci')
    def _check_unique_ci(self):
        for rec in self:
            if self.search([('ci', '=', rec.ci), ('id', '!=', rec.id)]):
                raise ValidationError("El CI ya está registrado.")

    @api.model
    def create(self, vals):
        if vals.get('cod_cliente', 'New') == 'New':
            vals['cod_cliente'] = self.env['ir.sequence'].next_by_code('internet.client') or 'New'
        return super(InternetClient, self).create(vals)
