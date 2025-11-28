from odoo import models, fields, api

class InternetSurvey(models.Model):
    _name = "internet.survey"
    _description = "Encuesta de Satisfacción del Cliente"
    _rec_name = 'client_id'
    
    

    client_id = fields.Many2one('internet.client', string='Cliente', required=True)
    survey_code = fields.Char('Código', readonly=True, copy=False, default='New')
    
    
    survey_chanel= fields.Selection([
        ('telefono', 'Teléfono'),
        ('email', 'Correo Electrónico'),
        ('presencial', 'Presencial'),
        ('whatsapp', 'WhatsApp'),
    ], string='Canal de la Encuesta', required=True)    
    
    survey_date = fields.Date('Fecha de la Encuesta', default=fields.Date.context_today, required=True)
    satisfaction_level = fields.Selection([
        ('muy_satisfecho', 'Muy Satisfecho'),
        ('satisfecho', 'Satisfecho'),
        ('neutral', 'Neutral'),
        ('insatisfecho', 'Insatisfecho'),
        ('muy_insatisfecho', 'Muy Insatisfecho'),
    ], string='Nivel de Satisfacción', required=True)
    comments = fields.Text('Comentarios Adicionales')
    surveyor_id = fields.Many2one('res.users', string='Encuestador', default=lambda self: self.env.user)
    internet_speed = fields.Selection([
        ('excelente', 'Excelente'),
        ('buena', 'Buena'),
        ('regular', 'Regular'),
        ('mala', 'Mala'),
        ('muy_mala', 'Muy Mala'),
    ], string='Velocidad de Internet Percibida', required=True) 
    atention_quality = fields.Selection([
        ('excelente', 'Excelente'),
        ('buena', 'Buena'),
        ('regular', 'Regular'),
        ('mala', 'Mala'),
        ('muy_mala', 'Muy Mala'),
    ], string='Calidad de Atención Percibida', required=True)   
    
    response_time = fields.Selection([
        ('muy_rapido', 'Muy Rápido'),
        ('rapido', 'Rápido'),
        ('adecuado', 'Adecuado'),
        ('lento', 'Lento'),
        ('muy_lento', 'Muy Lento'),
    ], string='Tiempo de Respuesta Percibido', required=True)
    
    qualityprice_ratio = fields.Selection([
        ('excelente', 'Excelente'),
        ('buena', 'Buena'),
        ('regular', 'Regular'),
        ('mala', 'Mala'),
        ('muy_mala', 'Muy Mala'),
    ], string='Relación Calidad-Precio Percibida', required=True)
    
    service_reliability = fields.Selection([
        ('muy_confiable', 'Muy Confiable'),     
        ('confiable', 'Confiable'),
        ('neutral', 'Neutral'),
        ('poco_confiable', 'Poco Confiable'),
        ('nada_confiable', 'Nada Confiable'),
    ], string='Confiabilidad del Servicio Percibida', required=True)    

    recomedation_likelihood = fields.Selection([
        ('definitivamente_si', 'Definitivamente Sí'),
        ('probablemente_si', 'Probablemente Sí'),
        ('no_se', 'No Sé'),
        ('probablemente_no', 'Probablemente No'),
        ('definitivamente_no', 'Definitivamente No'),
    ], string='Probabilidad de Recomendación', required=True)
    
    
    resolution_status = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('resuelto', 'Resuelto'),
    ], string='Estado de Resolución', default='pendiente')
    
    survey_type = fields.Selection([
        ('periodica', 'Periódica'),
        ('post_instalacion', 'Post-Instalación'),
        ('post_soporte', 'Post-Soporte'),
        ('cancelacion', 'Cancelación'),
    ], string='Tipo de Encuesta', required=True)
    
    @api.model
    def create(self, vals):
        if vals.get('survey_code', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code('internet.survey')
            if sequence:
                vals['survey_code'] = hex(int(sequence))[2:].upper()
            else:
                vals['survey_code'] = 'New'
        return super().create(vals)