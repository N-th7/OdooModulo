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
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        """Override para expandir todos los grupos de estado"""
        res = super(Tickets, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
        
        if 'estado' in groupby:
            # Obtener todos los estados posibles
            estados_posibles = dict(self._fields['estado'].selection)
            estados_existentes = [grupo['estado'] for grupo in res if 'estado' in grupo]
            
            # Agregar estados faltantes
            for estado_key, estado_label in estados_posibles.items():
                if estado_key not in estados_existentes:
                    res.append({
                        'estado': estado_key,
                        'estado_count': 0,
                        '__domain': domain + [('estado', '=', estado_key)],
                    })
            
            # Ordenar según el orden deseado
            orden_estados = ['abierto', 'en_proceso', 'resuelto', 'cerrado']
            res.sort(key=lambda x: orden_estados.index(x.get('estado', 'abierto')) if x.get('estado') in orden_estados else 999)
        
        return res