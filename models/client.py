from odoo import models, fields, api

class InternetClient(models.Model):
    _name = 'internet.client'
    _description = 'Cliente de Internet'
    _rec_name = 'name'

    # Campo ID automático por secuencia
    id = fields.Char(
        'ID Cliente',
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('internet.client')
    )

    # Datos personales
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

    # Relación con contratos
    contract_ids = fields.One2many(
        'internet.contract',
        'client_id',
        string='Contratos'
    )

    # Cantidad de contratos para el smart button
    contract_count = fields.Integer(
        string='N° Contratos',
        compute='_compute_contract_count'
    )

    # Relación con facturas
    invoice_ids = fields.One2many('internet.invoice', 'client_id', string='Facturas')

    deuda_meses = fields.Integer('Meses adeudados', compute='_compute_deuda', store=True)

    # ---------------------------
    #       COMPUTES
    # ---------------------------

    @api.depends('invoice_ids.state')
    def _compute_deuda(self):
        for rec in self:
            impagas = rec.invoice_ids.filtered(lambda i: i.state == 'impaga')
            rec.deuda_meses = len(impagas)

    @api.depends('contract_ids')
    def _compute_contract_count(self):
        for rec in self:
            rec.contract_count = len(rec.contract_ids)

    # ---------------------------
    #       ACCIONES
    # ---------------------------

    def action_add_contract(self):
        """Abrir formulario de contrato con cliente preseleccionado"""
        self.ensure_one()
        return {
            'name': 'Nuevo Contrato',
            'type': 'ir.actions.act_window',
            'res_model': 'internet.contract',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_client_id': self.id},
        }
