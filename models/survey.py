from odoo import models, fields, api

class InternetSurvey(models.Model):
    _name = "internet.survey"
    _description = "Encuesta de Satisfacción del Cliente"
    _rec_name = 'client_id'

    client_id = fields.Many2one('internet.client', string='Cliente', required=True)
    survey_date = fields.Date('Fecha de la Encuesta', default=fields.Date.context_today, required=True)
    satisfaction_level = fields.Selection([
        ('muy_satisfecho', 'Muy Satisfecho'),
        ('satisfecho', 'Satisfecho'),
        ('neutral', 'Neutral'),
        ('insatisfecho', 'Insatisfecho'),
        ('muy_insatisfecho', 'Muy Insatisfecho'),
    ], string='Nivel de Satisfacción', required=True)
    comments = fields.Text('Comentarios Adicionales')
    follow_up_required = fields.Boolean('Requiere Seguimiento', default=False)
    follow_up_date = fields.Date('Fecha de Seguimiento')
    active = fields.Boolean('Activo', default=True)
    surveyor_id = fields.Many2one('res.users', string='Encuestador', default=lambda self: self.env.user)
    resolution_status = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('resuelto', 'Resuelto'),
    ], string='Estado de Resolución', default='pendiente')
    