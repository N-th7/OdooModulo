from odoo import models, fields, api

class Tickets(models.Model):
    _name = 'internet.tickets'
    _description = 'Tickets de Soporte'
    _order = 'fecha_reporte desc'

    cliente_id = fields.Many2one('internet.client', string='Cliente', required=True)
    contrato_id = fields.Many2one('internet.contract', string='Contrato')
    descripcion = fields.Text('Descripción', required=True)
    fecha_reporte = fields.Datetime('Fecha de Reporte', default=fields.Datetime.now, required=True)
    fecha_resolucion = fields.Datetime('Fecha de Resolución')
    estado = fields.Selection([
        ('abierto', 'Abierto'),
        ('en_proceso', 'En Proceso'),
        ('resuelto', 'Resuelto'),
        ('cerrado', 'Cerrado'),
    ], string='Estado', default='abierto', required=True)
    prioridad = fields.Selection([
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ], string='Prioridad', default='media', required=True)
    tecnico_asignado = fields.Many2one('res.users', string='Técnico Asignado')
    observaciones = fields.Text('Observaciones')
    color = fields.Integer('Color', default=0)

    name = fields.Char('Número de Ticket', readonly=True, default='Nuevo')

    def name_get(self):
        return [(rec.id, f"Ticket #{rec.id} - {rec.cliente_id.name if rec.cliente_id else 'Sin cliente'}") for rec in self]

    @api.model
    def _group_expand_estado(self, states, domain, order):
        """Expandir todos los estados en vista kanban, incluso si están vacíos"""
        return [key for key, value in self._fields['estado'].selection]